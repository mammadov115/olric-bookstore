from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={
                'class': 'w-full p-4 bg-gray-50 rounded-2xl border border-gray-100 focus:ring-2 focus:ring-primary focus:border-transparent transition-all outline-none text-secondary font-medium',
                'placeholder': 'Kitab haqqında təəssüratlarınızı bölüşün...',
                'rows': 4
            }),
        }
