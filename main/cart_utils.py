"""
Sepet yardımcı fonksiyonları
"""
from django.conf import settings


def get_cart(request):
    """Sepeti session'dan al"""
    cart = request.session.get('cart', {})
    return cart


def add_to_cart(request, product_id, product_name):
    """Sepete ürün ekle"""
    cart = get_cart(request)
    
    # product_id'yi string'e çevir (session'da string olarak tutuluyor)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'name': product_name,
            'quantity': 1
        }
    
    request.session['cart'] = cart
    request.session.modified = True
    return cart


def update_cart_quantity(request, product_id, quantity):
    """Sepetteki ürün adedini güncelle"""
    cart = get_cart(request)
    
    # product_id'yi string'e çevir (session'da string olarak tutuluyor)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        if quantity <= 0:
            # Adet 0 veya daha azsa ürünü sepetten çıkar
            del cart[product_id_str]
        else:
            cart[product_id_str]['quantity'] = quantity
        request.session['cart'] = cart
        request.session.modified = True
    
    return cart


def remove_from_cart(request, product_id):
    """Sepetten ürün çıkar"""
    cart = get_cart(request)
    
    # product_id'yi string'e çevir (session'da string olarak tutuluyor)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
    
    return cart


def clear_cart(request):
    """Sepeti temizle"""
    request.session['cart'] = {}
    request.session.modified = True


def get_cart_count(request):
    """Sepetteki toplam ürün sayısı"""
    cart = get_cart(request)
    return sum(item['quantity'] for item in cart.values())


def get_cart_items(request):
    """Sepetteki ürünleri Product modeli ile birlikte döndür"""
    from .models import Product
    
    cart = get_cart(request)
    cart_items = []
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'name': item_data['name']
            })
        except Product.DoesNotExist:
            # Ürün bulunamazsa sepetten çıkar
            remove_from_cart(request, product_id)
    
    return cart_items

