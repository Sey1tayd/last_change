from django.shortcuts import render
from .models import CarouselItem


def home(request):
    """Ana sayfa görünümü"""
    carousel_items = CarouselItem.objects.filter(is_active=True).order_by('order', 'created_at')
    
    context = {
        'carousel_items': carousel_items,
    }
    return render(request, 'main/home.html', context)

