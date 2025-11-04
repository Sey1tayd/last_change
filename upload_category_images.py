"""
static/images klasöründeki resimleri kategori isimlerine göre eşleştirip Category modeline kaydeden script
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

from main.models import Category
from django.core.files import File
from pathlib import Path
from django.utils.text import slugify

def get_category_from_filename(filename):
    """
    Dosya ismine göre kategori belirler
    """
    filename_lower = filename.lower()
    name_without_ext = os.path.splitext(filename)[0].lower()
    
    # Kategori eşleştirmeleri - home.html'deki kategorilere göre
    category_mapping = {
        'at-kosu-ekipmanlari': {
            'keywords': ['eyer', 'eyeri', 'kapiton', 'uzengi', 'uzengi_kayisi', 'martingal', 
                        'martingalli', 'gogusluk', 'kece', 'pelus', 'eyer_ustu'],
            'display_name': 'AT KOŞU EKİPMANLARI'
        },
        'timar-ekipmanlari': {
            'keywords': ['firca', 'gebre', 'kasagi', 'tarak', 'bicagi', 'tuy', 'tuy_topla'],
            'display_name': 'TIMAR EKİPMANLARI'
        },
        'at-bakim-ekipmanlari': {
            'keywords': ['bandaj', 'absorbine', 'animalintex', 'cool_cast', 'powerflex', 
                        'polar', 'red_cell', 'apple_elite', 'sole_pack', 'libero', 
                        'tirnak', 'yag', 'maya', 'temizleme', 'ter_blanketi', 'ter', 'blanketi'],
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
    
    # Özel durumlar
    if 'gem' in filename_lower or 'gemi' in filename_lower:
        return 'at-kosu-ekipmanlari', 'AT KOŞU EKİPMANLARI'
    if 'baslik' in filename_lower or 'dizgin' in filename_lower:
        return 'at-kosu-ekipmanlari', 'AT KOŞU EKİPMANLARI'
    if 'yular' in filename_lower:
        return 'at-kosu-ekipmanlari', 'AT KOŞU EKİPMANLARI'
    if 'suluk' in filename_lower:
        return 'at-bakim-ekipmanlari', 'AT BAKIM EKİPMANLARI'
    if 'kolon' in filename_lower or 'getir' in filename_lower or 'belleme' in filename_lower:
        return 'timar-ekipmanlari', 'TIMAR EKİPMANLARI'
    if 'ahir' in filename_lower or 'culu' in filename_lower:
        return 'timar-ekipmanlari', 'TIMAR EKİPMANLARI'
    if 'western' in filename_lower:
        return 'at-kosu-ekipmanlari', 'AT KOŞU EKİPMANLARI'
    
    return None, None

def upload_category_images():
    """
    static/images klasöründeki resimleri kategorilere göre eşleştirip Category modeline kaydeder
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
    
    # Her kategori için en uygun resmi bul
    category_images = {}
    
    for img_file in image_files:
        category_slug, category_name = get_category_from_filename(img_file.name)
        
        if not category_slug or category_slug not in categories:
            continue
        
        # Eğer bu kategori için henüz resim seçilmediyse veya
        # Bu resim daha uygun görünüyorsa (kategori ismi ile daha uyumlu)
        if category_slug not in category_images:
            category_images[category_slug] = img_file
        else:
            # Kategori ismi ile daha uyumlu olanı seç
            current_img_name = category_images[category_slug].name.lower()
            new_img_name = img_file.name.lower()
            
            # Kategori isminin kelimelerini kontrol et
            category_keywords = category_names[category_slug].lower().split()
            current_match = sum(1 for kw in category_keywords if kw[:4] in current_img_name)
            new_match = sum(1 for kw in category_keywords if kw[:4] in new_img_name)
            
            if new_match > current_match:
                category_images[category_slug] = img_file
    
    # Kategori görsellerini kaydet
    updated_count = 0
    created_count = 0
    
    for category_slug, img_file in category_images.items():
        category = categories[category_slug]
        
        try:
            # Dosyayı Django FileField'a kaydet
            with open(img_file, 'rb') as f:
                django_file = File(f, name=img_file.name)
                category.image.save(img_file.name, django_file, save=True)
            
            if category.image:
                print(f"✓ {category.name} kategorisine görsel eklendi: {img_file.name}")
                updated_count += 1
            else:
                print(f"✗ {category.name} kategorisine görsel eklenemedi: {img_file.name}")
        except Exception as e:
            print(f"✗ Hata ({category.name} - {img_file.name}): {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"Özet:")
    print(f"  ✓ Kategori görseli güncellendi: {updated_count}")
    print(f"  📁 Toplam kategori: {len(categories)}")
    print(f"{'='*60}")
    print("\nKategori görselleri Railway'e deploy edildiğinde otomatik olarak yüklenecek.")

if __name__ == '__main__':
    upload_category_images()

