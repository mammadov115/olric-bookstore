from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone', 'address', 
            'city', 'postal_code', 'customer_notes', 'payment_method'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Ad və Soyad',
                'class': 'w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-4 text-sm focus:outline-none focus:ring-2 focus:ring-penguin-orange'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email ünvanı',
                'class': 'w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-4 text-sm focus:outline-none focus:ring-2 focus:ring-penguin-orange'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Telefon nömrəsi',
                'class': 'w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-4 text-sm focus:outline-none focus:ring-2 focus:ring-penguin-orange'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Tam ünvan',
                'rows': 3,
                'class': 'w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-4 text-sm focus:outline-none focus:ring-2 focus:ring-penguin-orange'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Şəhər',
                'class': 'w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-4 text-sm focus:outline-none focus:ring-2 focus:ring-penguin-orange'
            }),
            'postal_code': forms.TextInput(attrs={
                'placeholder': 'Poçt indeksi',
                'class': 'w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-4 text-sm focus:outline-none focus:ring-2 focus:ring-penguin-orange'
            }),
            'customer_notes': forms.Textarea(attrs={
                'placeholder': 'Kuryer üçün qeydlər (isteğe bağlı)',
                'rows': 2,
                'class': 'w-full bg-gray-50 border border-gray-100 rounded-xl px-4 py-4 text-sm focus:outline-none focus:ring-2 focus:ring-penguin-orange'
            }),
            'payment_method': forms.RadioSelect(attrs={'class': 'hidden peer'})
        }
