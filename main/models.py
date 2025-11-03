from django.db import models


class CarouselItem(models.Model):
    """Carousel'de gösterilecek Sketchfab model öğesi"""
    model_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Sketchfab Model ID",
        help_text="Sketchfab model ID'si (örn: 07882e7524534be984ae3e7faca25517)"
    )
    title = models.CharField(
        max_length=200,
        default="DESIGN SLIDER",
        verbose_name="Başlık"
    )
    topic = models.CharField(
        max_length=200,
        default="Model",
        verbose_name="Konu"
    )
    description = models.TextField(
        default="Lorem ipsum dolor sit amet consectetur adipisicing elit. Officia, laborum cumque dignissimos quidem atque et eligendi aperiam voluptates beatae maxime.",
        verbose_name="Açıklama"
    )
    detail_title = models.CharField(
        max_length=200,
        default="Model",
        verbose_name="Detay Başlığı"
    )
    detail_description = models.TextField(
        default="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dolor, reiciendis suscipit nobis nulla animi, modi explicabo quod corrupti impedit illo, accusantium in eaque nam quia adipisci aut distinctio porro eligendi.",
        verbose_name="Detay Açıklaması"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sıralama",
        help_text="Carousel'de görünecek sıra (0 en başta)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif",
        help_text="Carousel'de gösterilsin mi?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carousel Öğesi"
        verbose_name_plural = "Carousel Öğeleri"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.topic} ({self.model_id})"
