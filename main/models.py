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


class Category(models.Model):
    """Ürün kategorileri"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Kategori Adı"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Slug"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Açıklama"
    )
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        verbose_name="Kategori Görseli",
        help_text="Kategori kartında gösterilecek görsel"
    )
    image_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Kategori Görseli URL",
        help_text="Eğer görsel dosyası yoksa URL kullanın"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sıralama"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
    
    @property
    def get_image_url(self):
        """Görsel URL'ini döndürür - önce yüklenen görsel, sonra URL"""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return None


class Product(models.Model):
    """Ürün modeli"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Kategori"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Ürün Adı"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Açıklama"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Fiyat"
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="Ürün Görseli"
    )
    image_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Görsel URL",
        help_text="Eğer görsel dosyası yoksa URL kullanın"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Öne Çıkan",
        help_text="Öne çıkan ürünler bölümünde gösterilsin mi?"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktif"
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stok"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.name

    @property
    def get_image_url(self):
        """Görsel URL'ini döndürür"""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return None


class Order(models.Model):
    """Sipariş modeli"""
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('confirmed', 'Onaylandı'),
        ('cancelled', 'İptal Edildi'),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Ürün"
    )
    customer_name = models.CharField(
        max_length=100,
        verbose_name="Müşteri Adı"
    )
    customer_phone = models.CharField(
        max_length=20,
        verbose_name="Telefon"
    )
    customer_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="E-posta"
    )
    customer_address = models.TextField(
        verbose_name="Adres"
    )
    message = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mesaj/Not"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Durum"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.product.name} ({self.get_status_display()})"