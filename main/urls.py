from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kategori/<slug:slug>/', views.category_detail, name='category_detail'),
    path('urun/<slug:slug>/', views.product_detail, name='product_detail'),
    path('ara/', views.search, name='search'),
]

