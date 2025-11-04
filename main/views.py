from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings
from .models import CarouselItem, Category, Product, Order
from .forms import OrderForm
from .cart_utils import (
    add_to_cart, remove_from_cart, clear_cart,
    get_cart_count, get_cart_items, get_cart,
    update_cart_quantity
)
import random
import json


def home(request):
    """Ana sayfa görünümü"""
    carousel_items = CarouselItem.objects.filter(is_active=True).order_by('order', 'created_at')
    
    # Her kategoriden 2-3 ürün rastgele seç, toplam ~15 ürün
    featured_products = []
    categories = Category.objects.filter(is_active=True)
    
    for category in categories:
        category_products = Product.objects.filter(
            category=category,
            is_active=True,
            is_featured=True
        )
        if category_products.exists():
            # Her kategoriden 2-3 ürün rastgele seç
            count = random.randint(2, 3)
            selected = list(category_products)
            random.shuffle(selected)
            featured_products.extend(selected[:count])
    
    # Eğer featured ürünler yoksa, normal aktif ürünlerden seç
    if len(featured_products) < 15:
        remaining = 15 - len(featured_products)
        additional_products = Product.objects.filter(
            is_active=True
        ).exclude(id__in=[p.id for p in featured_products])
        if additional_products.exists():
            additional = list(additional_products)
            random.shuffle(additional)
            featured_products.extend(additional[:remaining])
    
    # Toplam 15 ürünü aşmayacak şekilde karıştır
    random.shuffle(featured_products)
    featured_products = featured_products[:15]
    
    # Aktif kategorileri al
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'carousel_items': carousel_items,
        'featured_products': featured_products,
        'categories': categories,
        'cart_count': get_cart_count(request),
    }
    return render(request, 'main/home.html', context)


def category_detail(request, slug):
    """Kategori detay sayfası"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True).order_by('-is_featured', '-created_at')
    
    # Tüm kategorileri menü için al
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'cart_count': get_cart_count(request),
    }
    return render(request, 'main/category_detail.html', context)


def product_detail(request, slug):
    """Ürün detay sayfası"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Aynı kategorideki benzer ürünler
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).order_by('-is_featured', '-created_at')[:8]
    
    # Tüm kategorileri menü için al
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'product': product,
        'related_products': related_products,
        'categories': categories,
        'whatsapp_phone': getattr(settings, 'WHATSAPP_PHONE', '905350434796'),
        'cart_count': get_cart_count(request),
    }
    return render(request, 'main/product_detail.html', context)


def search(request):
    """Arama sayfası"""
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).filter(is_active=True).order_by('-is_featured', '-created_at')
    
    # Tüm kategorileri menü için al
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'query': query,
        'products': products,
        'categories': categories,
        'cart_count': get_cart_count(request),
    }
    return render(request, 'main/search.html', context)


@require_http_methods(["POST"])
def add_to_cart_view(request):
    """Sepete ürün ekle (AJAX)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            product_name = data.get('product_name')
            
            if not product_id or not product_name:
                return JsonResponse({'success': False, 'error': 'Eksik bilgi'}, status=400)
            
            add_to_cart(request, product_id, product_name)
            cart_count = get_cart_count(request)
            
            return JsonResponse({
                'success': True,
                'cart_count': cart_count,
                'message': 'Ürün sepete eklendi!'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Geçersiz istek'}, status=400)


def cart_view(request):
    """Sepet sayfası"""
    cart_items = get_cart_items(request)
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    whatsapp_phone = getattr(settings, 'WHATSAPP_PHONE', '905350434796')
    
    context = {
        'cart_items': cart_items,
        'categories': categories,
        'cart_count': get_cart_count(request),
        'whatsapp_phone': whatsapp_phone,
    }
    return render(request, 'main/cart.html', context)


@require_http_methods(["POST"])
def remove_from_cart_view(request, product_id):
    """Sepetten ürün çıkar"""
    remove_from_cart(request, product_id)
    cart_count = get_cart_count(request)
    
    return JsonResponse({
        'success': True,
        'cart_count': cart_count,
        'message': 'Ürün sepetten çıkarıldı'
    })


@require_http_methods(["POST"])
def update_quantity_view(request, product_id):
    """Sepetteki ürün adedini güncelle"""
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Adet en az 1 olmalı'}, status=400)
        
        # product_id'yi string'e çevir (session'da string olarak tutuluyor)
        product_id_str = str(product_id)
        update_cart_quantity(request, product_id_str, quantity)
        cart_count = get_cart_count(request)
        
        # Güncellenmiş ürün bilgisini al
        cart = get_cart(request)
        product_quantity = cart.get(product_id_str, {}).get('quantity', 0)
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'quantity': product_quantity,
            'message': 'Adet güncellendi'
        })
    except (ValueError, KeyError) as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def send_cart_whatsapp(request):
    """Sepetteki ürünleri WhatsApp ile gönder"""
    from urllib.parse import quote
    
    cart_items = get_cart_items(request)
    
    if not cart_items:
        messages.warning(request, 'Sepetiniz boş!')
        return redirect('cart')
    
    whatsapp_phone = getattr(settings, 'WHATSAPP_PHONE', '905350434796')
    
    # WhatsApp mesajı oluştur
    message_lines = [
        'Merhaba!',
        '',
        'Şu ürünlerden şu adetlerde istiyorum, bilgi alabilir miyim?',
        '',
        '📦 ÜRÜNLER:',
        ''
    ]
    
    total_quantity = 0
    for item in cart_items:
        product = item['product']
        quantity = item['quantity']
        total_quantity += quantity
        # Ürün linkini oluştur
        product_url = request.build_absolute_uri(f'/urun/{product.slug}/')
        message_lines.append(f'• {product.name} - {quantity} adet')
        message_lines.append(f'  {product_url}')
    
    message_lines.append('')
    message_lines.append(f'Toplam: {len(cart_items)} çeşit ürün, {total_quantity} adet')
    message_lines.append('')
    message_lines.append('Bilgi alabilir miyim?')
    
    message = '\n'.join(message_lines)
    
    # WhatsApp URL oluştur (encode edilmiş mesaj)
    encoded_message = quote(message)
    whatsapp_url = f'https://wa.me/{whatsapp_phone}?text={encoded_message}'
    
    # Sepeti temizle
    clear_cart(request)
    
    # WhatsApp'ı yeni sekmede aç
    return redirect(whatsapp_url)

