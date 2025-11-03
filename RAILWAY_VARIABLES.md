# Railway Environment Variables

Railway dashboard'da **Settings > Variables** bölümüne şu environment variables'ları ekle:

## Zorunlu Variables

### SECRET_KEY
```
django-insecure-RAILWAY-PRODUCTION-CHANGE-THIS-TO-RANDOM-STRING-MIN-50-CHAR
```
**Not:** Güvenli bir random string kullan (en az 50 karakter). Örnek oluşturmak için:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### DEBUG
```
False
```
Production için mutlaka `False` olmalı.

### ALLOWED_HOSTS
```
your-app-name.railway.app,*.railway.app
```
Railway'den aldığın domain'i buraya ekle. Örnek: `sarac-ihsan.railway.app`

## Database (Otomatik)

### DATABASE_URL
Railway'de PostgreSQL database eklediğinde otomatik olarak eklenir. Manuel eklemen gerekmez.

## Superuser Variables

### SUPERUSER_USERNAME
```
admin
```
Veya istediğin kullanıcı adı.

### SUPERUSER_EMAIL
```
admin@saracihsan.com
```
Veya admin e-posta adresi (opsiyonel).

### SUPERUSER_PASSWORD
```
GüvenliBirŞifre123!
```
Güçlü bir şifre kullan. Minimum 8 karakter, harf, rakam ve özel karakter içermeli.

---

## Hızlı Kurulum

Railway dashboard'da Variables sekmesine şunları ekle:

1. **SECRET_KEY** = `[Yukarıdaki komutla oluşturduğun random string]`
2. **DEBUG** = `False`
3. **ALLOWED_HOSTS** = `your-app-name.railway.app` (veya Railway'den aldığın domain)
4. **SUPERUSER_USERNAME** = `admin` (veya istediğin isim)
5. **SUPERUSER_EMAIL** = `admin@saracihsan.com` (opsiyonel)
6. **SUPERUSER_PASSWORD** = `[Güvenli bir şifre]`

**Not:** PostgreSQL database eklediğinde `DATABASE_URL` otomatik eklenir.

