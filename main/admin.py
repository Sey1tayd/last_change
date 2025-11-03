from django.contrib import admin
from .models import CarouselItem, Category, Product


@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ['topic', 'model_id', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['model_id', 'topic', 'title']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'created_at']
    
    fieldsets = (
        ('Sketchfab Model Bilgileri', {
            'fields': ('model_id', 'order', 'is_active')
        }),
        ('Görünüm Bilgileri', {
            'fields': ('title', 'topic', 'description')
        }),
        ('Detay Sayfası Bilgileri', {
            'fields': ('detail_title', 'detail_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'slug', 'description', 'image_url')
        }),
        ('Durum', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_featured', 'is_active', 'stock', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_featured', 'is_active', 'stock']
    ordering = ['-is_featured', '-created_at']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Fiyat ve Stok', {
            'fields': ('price', 'stock'),
            'classes': ('collapse',)
        }),
        ('Görsel', {
            'fields': ('image', 'image_url')
        }),
        ('Durum', {
            'fields': ('is_featured', 'is_active')
        }),
    )
