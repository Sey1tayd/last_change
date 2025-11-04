from .models import Category


def categories(request):
    """Tüm şablonlara kategorileri ekler"""
    return {
        'categories': Category.objects.filter(is_active=True).order_by('order', 'name')
    }

