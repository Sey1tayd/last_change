from django.contrib import admin
from .models import CarouselItem


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
