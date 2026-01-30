from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'bg-gray-50 border border-gray-100 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-penguin-orange text-penguin-navy font-bold w-full uppercase',
        'placeholder': 'Kupon Kodu'
    }))
