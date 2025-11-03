from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import CarouselItem, Category, Product
import random


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
    }
    return render(request, 'main/search.html', context)

