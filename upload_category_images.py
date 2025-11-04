"""
static/images klasöründeki resimleri kategori isimlerine göre eşleştirip Product olarak ekleyen script
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
from pathlib import Path

def get_category_from_filename(filename):
    """
    Dosya ismine göre kategori belirler - home.html'deki kategorilere göre
    """
    filename_lower = filename.lower()
    name_without_ext = os.path.splitext(filename)[0].lower()
    
    # Kategori eşleştirmeleri
    category_mapping = {
        'at-kosu-ekipmanlari': {
            'keywords': ['eyer', 'eyeri', 'kapiton', 'uzengi', 'uzengi_kayisi', 'martingal', 
                        'martingalli', 'gogusluk', 'kece', 'pelus', 'eyer_ustu', 'gem', 'gemi',
                        'baslik', 'dizgin', 'yular', 'western', 'kolon', 'getir', 'belleme'],
            'display_name': 'AT KOŞU EKİPMANLARI'
        },
        'timar-ekipmanlari': {
            'keywords': ['firca', 'gebre', 'kasagi', 'tarak', 'bicagi', 'tuy', 'tuy_topla',
                        'ahir', 'culu', 'ahir_bellemesi', 'ahir_culu'],
            'display_name': 'TIMAR EKİPMANLARI'
        },
        'at-bakim-ekipmanlari': {
            'keywords': ['bandaj', 'absorbine', 'animalintex', 'cool_cast', 'powerflex', 
                        'polar', 'red_cell', 'apple_elite', 'sole_pack', 'libero', 
                        'tirnak', 'yag', 'maya', 'temizleme', 'ter_blanketi', 'ter', 'blanketi',
                        'suluk'],
            'display_name': 'AT BAKIM EKİPMANLARI'
        },
        'nalbant-ekipmanlari': {
            'keywords': ['nal', 'nalbant', 'civi', 'cekic', 'pensesi', 'kerpeten', 'dovme', 
                        'seti', 'nal_dovme'],
            'display_name': 'NALBANT EKİPMANLARI'
        },
        'araba-fayton-takimi': {
            'keywords': ['araba', 'fayton', 'takimi', 'hamut'],
            'display_name': 'ARABA FAYTON TAKIMI'
        },
        'binici-ekipmanlari': {
            'keywords': ['binici', 'eldiven', 'tog', 'yeleg', 'maskesi', 'chaps', 'kampci', 
                        'mahmuz', 'bot', 'kask'],
            'display_name': 'BİNİCİ EKİPMANLARI'
        }
    }
    
    # Dosya ismini kontrol et
    for category_slug, category_info in category_mapping.items():
        for keyword in category_info['keywords']:
            if keyword in filename_lower or keyword in name_without_ext:
                return category_slug, category_info['display_name']
    
    return None, None

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

def upload_products_from_static_images():
    """
    static/images klasöründeki resimleri kategorilere göre ayırıp Product olarak ekler
    """
    # Klasör yolları
    base_dir = Path(__file__).parent
    static_images_dir = base_dir / 'static' / 'images'
    
    if not static_images_dir.exists():
        print(f"Hata: {static_images_dir} klasörü bulunamadı!")
        return
    
    # Tüm resim dosyalarını al
    image_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    image_files = []
    for ext in image_extensions:
        image_files.extend(list(static_images_dir.glob(f'*{ext}')))
    
    # Logo ve diğer sistem dosyalarını hariç tut
    excluded_files = ['logo.png', 'Sarac_Ihsan_At_Ekipmanlari.png', 'img1.png', 'img2.png', 
                      'img3.png', 'img4.png', 'img5.png', 'img6.png']
    image_files = [f for f in image_files if f.name not in excluded_files]
    
    if not image_files:
        print(f"static/images klasöründe resim bulunamadı!")
        return
    
    print(f"Toplam {len(image_files)} resim bulundu.\n")
    
    # Kategorileri al veya oluştur
    categories = {}
    category_names = {
        'at-kosu-ekipmanlari': 'AT KOŞU EKİPMANLARI',
        'timar-ekipmanlari': 'TIMAR EKİPMANLARI',
        'at-bakim-ekipmanlari': 'AT BAKIM EKİPMANLARI',
        'nalbant-ekipmanlari': 'NALBANT EKİPMANLARI',
        'araba-fayton-takimi': 'ARABA FAYTON TAKIMI',
        'binici-ekipmanlari': 'BİNİCİ EKİPMANLARI'
    }
    
    for slug, name in category_names.items():
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            try:
                category = Category.objects.get(name=name)
            except Category.DoesNotExist:
                category = Category.objects.create(
                    name=name,
                    slug=slug,
                    description=f'{name} kategorisi',
                    is_active=True,
                    order=len(categories)
                )
                print(f"✓ Yeni kategori oluşturuldu: {name}")
        categories[slug] = category
    
    print()
    
    # Ürünleri oluştur
    created_count = 0
    updated_count = 0
    skipped_count = 0
    
    for img_file in image_files:
        try:
            # Kategori belirle
            category_slug, category_name = get_category_from_filename(img_file.name)
            
            if not category_slug or category_slug not in categories:
                print(f"⚠ Kategori bulunamadı: {img_file.name}")
                skipped_count += 1
                continue
            
            category = categories[category_slug]
            
            # Ürün adı ve slug oluştur
            product_name = clean_product_name(img_file.name)
            product_slug = slugify(product_name)
            
            # Static URL oluştur
            static_url = f"/static/images/{img_file.name}"
            
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

if __name__ == '__main__':
    try:
        upload_products_from_static_images()
    except Exception as e:
        print(f"⚠ Ürünler yüklenirken hata oluştu: {str(e)}")
        print("Deploy devam ediyor...")
        # Hata olsa bile deploy'un devam etmesi için exit(0)
        import sys
        sys.exit(0)
