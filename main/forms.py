from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """Sipariş formu"""
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_email', 'customer_address', 'message']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız Soyadınız',
                'required': True
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Telefon Numaranız',
                'required': True,
                'type': 'tel'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-posta Adresiniz (Opsiyonel)',
                'type': 'email'
            }),
            'customer_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Teslimat Adresiniz',
                'rows': 4,
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Eklemek istediğiniz notlar (Opsiyonel)',
                'rows': 3
            }),
        }
        labels = {
            'customer_name': 'Ad Soyad',
            'customer_phone': 'Telefon',
            'customer_email': 'E-posta',
            'customer_address': 'Adres',
            'message': 'Mesaj/Not',
        }

