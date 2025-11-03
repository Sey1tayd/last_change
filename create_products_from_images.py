"""
Images klasöründeki resimlerden ürün oluşturma scripti
"""
import os
import sys
import django

# Windows'ta encoding sorununu çöz
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Django setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sarac_ihsan.settings')
django.setup()

from main.models import Category, Product
from django.utils.text import slugify

def create_products_from_images():
    """static/images klasöründeki resimlerden ürün oluştur"""
    
    # Varsayılan kategori oluştur veya al
    default_category, created = Category.objects.get_or_create(
        slug='genel',
        defaults={
            'name': 'Genel',
            'description': 'Genel ürünler',
            'is_active': True
        }
    )
    
    if created:
        print(f"Varsayılan kategori oluşturuldu: {default_category.name}")
    
    # Images klasöründeki resimleri al
    images_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
    image_files = ['img1.png', 'img2.png', 'img3.png', 'img4.png', 'img5.png', 'img6.png']
    
    created_count = 0
    updated_count = 0
    
    for img_file in image_files:
        img_path = os.path.join(images_dir, img_file)
        
        # Dosya var mı kontrol et
        if not os.path.exists(img_path):
            print(f"Uyarı: {img_file} bulunamadı, atlanıyor...")
            continue
        
        # Ürün adı oluştur (img1.png -> Ürün 1)
        product_number = img_file.replace('img', '').replace('.png', '')
        product_name = f"Ürün {product_number}"
        product_slug = slugify(product_name)
        
        # Static URL oluştur
        static_url = f"/static/images/{img_file}"
        
        # Ürün var mı kontrol et
        product, created = Product.objects.get_or_create(
            slug=product_slug,
            defaults={
                'category': default_category,
                'name': product_name,
                'description': f"{product_name} için açıklama",
                'image_url': static_url,
                'is_featured': True,  # Öne çıkan olarak işaretle
                'is_active': True,
                'stock': 0
            }
        )
        
        if created:
            print(f"✓ Ürün oluşturuldu: {product_name} ({img_file})")
            created_count += 1
        else:
            # Mevcut ürünü güncelle
            product.image_url = static_url
            product.is_featured = True
            product.is_active = True
            product.save()
            print(f"↻ Ürün güncellendi: {product_name} ({img_file})")
            updated_count += 1
    
    print(f"\nToplam: {created_count} yeni ürün oluşturuldu, {updated_count} ürün güncellendi.")
    print(f"Tüm ürünler '{default_category.name}' kategorisine eklendi ve öne çıkan olarak işaretlendi.")

if __name__ == '__main__':
    create_products_from_images()

