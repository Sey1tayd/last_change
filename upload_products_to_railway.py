"""
Upload klasöründeki resimleri dosya isimlerine göre kategorilere ayırıp Railway'e yükleme scripti
"""
import os
import sys
import shutil
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
from pathlib import Path

def get_category_from_filename(filename):
    """
    Dosya ismine göre kategori belirler
    """
    filename_lower = filename.lower()
    name_without_ext = os.path.splitext(filename)[0]
    
    # Kategori eşleştirmeleri
    category_mapping = {
        'eyer': ['eyer', 'eyeri'],
        'gem': ['gem', 'gemi'],
        'baslik_dizgin': ['baslik', 'dizgin'],
        'yular': ['yular'],
        'nal': ['nal'],
        'binici_ekipmanlari': ['binici', 'eldiven', 'tog', 'yeleg', 'maskesi', 'chaps'],
        'ahir_ekipmanlari': ['ahir', 'belleme', 'kolon', 'culu', 'getir'],
        'bakim_urunleri': ['firca', 'gebre', 'bicagi', 'bandaj', 'absorbine', 'animalintex', 
                          'cool_cast', 'powerflex', 'polar', 'red_cell', 'apple_elite', 
                          'sole_pack', 'libero', 'tirnak', 'yag', 'maya', 'temizleme'],
        'western_ekipmanlari': ['western', 'boncuklu', 'gumuslu', 'sade'],
        'suluk': ['suluk'],
        'uzengi': ['uzengi'],
        'martingal': ['martingal', 'martingalli'],
        'kece': ['kece'],
        'ter_blanketi': ['ter', 'blanketi'],
        'nalbant_araclari': ['nalbant', 'civi', 'cekic', 'pensesi', 'kerpeten', 'dovme'],
    }
    
    # Dosya ismini kontrol et
    for category_key, keywords in category_mapping.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return category_key
    
    # Özel durumlar
    if 'kapiton' in filename_lower:
        return 'eyer'
    if 'hamut' in filename_lower:
        return 'ahir_ekipmanlari'
    if 'kampa' in filename_lower:
        return 'binici_ekipmanlari'
    
    # Varsayılan kategori
    return 'diger'

def get_category_display_name(category_key):
    """
    Kategori key'ini Türkçe isme çevirir
    """
    category_names = {
        'eyer': 'Eyerler',
        'gem': 'Gemler',
        'baslik_dizgin': 'Başlık ve Dizginler',
        'yular': 'Yularlar',
        'nal': 'Naller',
        'binici_ekipmanlari': 'Binici Ekipmanları',
        'ahir_ekipmanlari': 'Ahır Ekipmanları',
        'bakim_urunleri': 'Bakım Ürünleri',
        'western_ekipmanlari': 'Western Ekipmanları',
        'suluk': 'Suluklar',
        'uzengi': 'Üzengiler',
        'martingal': 'Martingaller',
        'kece': 'Keçeler',
        'ter_blanketi': 'Ter Örtüleri',
        'nalbant_araclari': 'Nalbant Araçları',
        'diger': 'Diğer Ürünler',
    }
    return category_names.get(category_key, 'Diğer Ürünler')

def clean_product_name(filename):
    """
    Dosya isminden ürün adı oluşturur
    """
    name_without_ext = os.path.splitext(filename)[0]
    # Alt çizgileri boşlukla değiştir ve başlık formatına çevir
    name = name_without_ext.replace('_', ' ')
    # İlk harfleri büyük yap
    name = ' '.join(word.capitalize() for word in name.split())
    return name

def upload_products_from_upload_folder():
    """
    Upload klasöründeki resimleri kategorilere ayırıp ürünleri oluşturur
    """
    # Klasör yolları
    base_dir = Path(__file__).parent
    upload_dir = base_dir / 'upload'
    static_images_dir = base_dir / 'static' / 'images'
    
    # Static/images klasörünü oluştur
    static_images_dir.mkdir(parents=True, exist_ok=True)
    
    if not upload_dir.exists():
        print(f"Hata: {upload_dir} klasörü bulunamadı!")
        return
    
    # Tüm resim dosyalarını al
    image_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    image_files = []
    for ext in image_extensions:
        image_files.extend(list(upload_dir.glob(f'*{ext}')))
    
    if not image_files:
        print(f"Upload klasöründe resim bulunamadı!")
        return
    
    print(f"Toplam {len(image_files)} resim bulundu.\n")
    
    # Kategorileri oluştur
    categories = {}
    category_keys = set()
    
    for img_file in image_files:
        category_key = get_category_from_filename(img_file.name)
        category_keys.add(category_key)
    
    # Her kategori için Category oluştur
    for category_key in category_keys:
        category_name = get_category_display_name(category_key)
        category_slug = slugify(category_key)
        
        # Önce slug'a göre kontrol et
        try:
            category = Category.objects.get(slug=category_slug)
            created = False
        except Category.DoesNotExist:
            # Slug yoksa name'e göre kontrol et
            try:
                category = Category.objects.get(name=category_name)
                created = False
            except Category.DoesNotExist:
                # Yeni kategori oluştur
                category = Category.objects.create(
                    name=category_name,
                    slug=category_slug,
                    description=f'{category_name} kategorisi',
                    is_active=True,
                    order=len(categories)
                )
                created = True
        
        categories[category_key] = category
        
        if created:
            print(f"✓ Kategori oluşturuldu: {category_name}")
        else:
            print(f"↻ Kategori mevcut: {category_name}")
    
    print()
    
    # Ürünleri oluştur
    created_count = 0
    updated_count = 0
    skipped_count = 0
    
    for img_file in image_files:
        try:
            # Kategori belirle
            category_key = get_category_from_filename(img_file.name)
            category = categories.get(category_key)
            
            if not category:
                print(f"⚠ Kategori bulunamadı: {img_file.name}")
                skipped_count += 1
                continue
            
            # Ürün adı ve slug oluştur
            product_name = clean_product_name(img_file.name)
            product_slug = slugify(product_name)
            
            # Resmi static/images klasörüne kopyala
            dest_path = static_images_dir / img_file.name
            
            # Eğer dosya zaten varsa, benzersiz isim oluştur
            counter = 1
            original_dest = dest_path
            while dest_path.exists():
                name_part = os.path.splitext(img_file.name)[0]
                ext_part = os.path.splitext(img_file.name)[1]
                new_name = f"{name_part}_{counter}{ext_part}"
                dest_path = static_images_dir / new_name
            
            # Dosyayı kopyala
            shutil.copy2(img_file, dest_path)
            
            # Static URL oluştur
            static_url = f"/static/images/{dest_path.name}"
            
            # Ürün oluştur veya güncelle
            product, created = Product.objects.get_or_create(
                slug=product_slug,
                defaults={
                    'category': category,
                    'name': product_name,
                    'description': f"{product_name} ürünü",
                    'image_url': static_url,
                    'is_active': True,
                    'stock': 0
                }
            )
            
            if created:
                print(f"✓ Ürün oluşturuldu: {product_name} → {category.name} ({img_file.name})")
                created_count += 1
            else:
                # Mevcut ürünü güncelle
                product.image_url = static_url
                product.category = category
                product.is_active = True
                product.save()
                print(f"↻ Ürün güncellendi: {product_name} → {category.name} ({img_file.name})")
                updated_count += 1
                
        except Exception as e:
            print(f"✗ Hata ({img_file.name}): {str(e)}")
            skipped_count += 1
    
    print(f"\n{'='*60}")
    print(f"Özet:")
    print(f"  ✓ Yeni ürün oluşturuldu: {created_count}")
    print(f"  ↻ Mevcut ürün güncellendi: {updated_count}")
    print(f"  ✗ Atlandı: {skipped_count}")
    print(f"  📦 Toplam işlenen: {created_count + updated_count}")
    print(f"{'='*60}")
    print("\nResimler static/images klasörüne kopyalandı.")
    print("Railway'e deploy ettiğinizde collectstatic komutu ile bu dosyalar staticfiles klasörüne toplanacak.")

if __name__ == '__main__':
    upload_products_from_upload_folder()

