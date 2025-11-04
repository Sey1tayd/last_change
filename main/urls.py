from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kategori/<slug:slug>/', views.category_detail, name='category_detail'),
    path('urun/<slug:slug>/', views.product_detail, name='product_detail'),
    path('ara/', views.search, name='search'),
    path('sepet/', views.cart_view, name='cart'),
    path('sepet/ekle/', views.add_to_cart_view, name='add_to_cart'),
    path('sepet/cikar/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('sepet/adet/<int:product_id>/', views.update_quantity_view, name='update_quantity'),
    path('sepet/whatsapp/', views.send_cart_whatsapp, name='send_cart_whatsapp'),
]

