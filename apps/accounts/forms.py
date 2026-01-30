from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name", "phone")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Use email as username for uniqueness
        if commit:
            user.save()
        return user