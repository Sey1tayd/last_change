# Sarac İhsan - At Ekipmanları Satış Sitesi

Django tabanlı web sitesi projesi.

## Kurulum

1. Sanal ortam oluştur:
```bash
python -m venv venv
```

2. Sanal ortamı aktifleştir:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Gereksinimleri yükle:
```bash
pip install -r requirements.txt
```

4. Veritabanını oluştur:
```bash
python manage.py migrate
```

5. Sunucuyu başlat:
```bash
python manage.py runserver
```

Site http://localhost:8000 adresinde çalışacaktır.

## Railway'e Deploy Etme

Bu proje Railway'de çalışacak şekilde yapılandırılmıştır.

### Adımlar:

1. **GitHub'a push et:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Sey1tayd/last_change.git
git push -u origin main
```

2. **Railway'de yeni proje oluştur:**
   - Railway.app'e git
   - "New Project" > "Deploy from GitHub repo" seç
   - Repository'ni seç

3. **Environment Variables ekle:**
   Railway dashboard'da Settings > Variables bölümüne şunları ekle:
   
   **Zorunlu Variables:**
   - `SECRET_KEY`: Django secret key (güvenli bir random string, en az 50 karakter)
   - `DEBUG`: `False` (production için)
   - `ALLOWED_HOSTS`: Railway domain'in (örn: `your-app-name.railway.app`)
   
   **Superuser Variables:**
   - `SUPERUSER_USERNAME`: Admin kullanıcı adı (örn: `admin`)
   - `SUPERUSER_EMAIL`: Admin e-posta (opsiyonel, örn: `admin@saracihsan.com`)
   - `SUPERUSER_PASSWORD`: Admin şifresi (güvenli bir şifre)
   
   Detaylı bilgi için `RAILWAY_VARIABLES.md` dosyasına bak.

4. **PostgreSQL ekle (opsiyonel):**
   - Railway'de "New" > "Database" > "Add PostgreSQL"
   - `DATABASE_URL` otomatik olarak environment variable olarak eklenir

5. **Deploy:**
   - Railway otomatik olarak deploy edecek
   - İlk deploy'ta migration'lar ve collectstatic otomatik çalışır

### Notlar:
- Static files WhiteNoise ile otomatik servis edilir
- PostgreSQL varsa otomatik kullanılır, yoksa SQLite kullanılır (development)
- Gunicorn production server olarak kullanılır

