from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', _('Customer')
        COURIER = 'courier', _('Courier')
        ADMIN = 'admin', _('Admin')

    # Username sahəsini deaktiv etmək üçün null=True və blank=True edirik (və ya tam silirik)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Toqquşmaları həll edən related_name-lər
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_permissions",
        blank=True
    )

    # Profile Fields (Merged)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    social_links = models.JSONField(default=dict, blank=True)

    objects = UserManager() # 👈 Manager-i buraya bağlayırıq

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Email artıq avtomatik tələb olunur

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

