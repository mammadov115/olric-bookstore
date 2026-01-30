from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from apps.accounts.models import User, Profile
from apps.accounts.forms import UserRegisterForm

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('books:home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.object)
        return redirect(self.get_success_url())

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    fields = ['bio', 'birth_date', 'preferences']
    success_url = reverse_lazy('books:home')

    def get_object(self, queryset=None):
        return self.request.user.profile