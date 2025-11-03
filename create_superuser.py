"""
Railway deploy sırasında superuser oluşturmak için script.
Environment variables'dan SUPERUSER_USERNAME, SUPERUSER_EMAIL ve SUPERUSER_PASSWORD okur.
"""
import os
import sys
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sarac_ihsan.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    username = os.environ.get('SUPERUSER_USERNAME')
    email = os.environ.get('SUPERUSER_EMAIL', '')
    password = os.environ.get('SUPERUSER_PASSWORD')
    
    if not username or not password:
        print("SUPERUSER_USERNAME ve SUPERUSER_PASSWORD environment variables gereklidir.")
        return
    
    # Eğer superuser zaten varsa oluşturma
    if User.objects.filter(username=username).exists():
        print(f"Superuser '{username}' zaten mevcut.")
        return
    
    try:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"Superuser '{username}' başarıyla oluşturuldu.")
    except Exception as e:
        print(f"Superuser oluşturulurken hata: {e}")

if __name__ == '__main__':
    create_superuser()

