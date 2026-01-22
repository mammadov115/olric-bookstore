from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from apps.accounts.models import User, Profile
from apps.accounts.forms import UserRegisterForm # Bu formanı aşağıda tərif edəcəyik

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # İstifadəçini qeyd et və dərhal giriş etdir
        response = super().form_valid(form)
        # Backend sahəsini təyin et və login et
        self.object.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.object)
        return response

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    fields = ['bio', 'birth_date', 'preferences']
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        # Login olan istifadəçinin öz profilini qaytarır
        return self.request.user.profile