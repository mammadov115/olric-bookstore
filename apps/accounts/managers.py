from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """Custom manager for Olric User model with no username field."""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email mütləq daxil edilməlidir')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser mütləq is_staff=True olmalıdır.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser mütləq is_superuser=True olmalıdır.')

        return self._create_user(email, password, **extra_fields)
