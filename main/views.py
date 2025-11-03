from django.shortcuts import render


def home(request):
    """Ana sayfa görünümü"""
    return render(request, 'main/home.html')

