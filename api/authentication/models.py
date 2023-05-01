from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
        

ROLE = (
    ('farmer', 'Farmer'),
    ('customer', 'Customer'),
)

class UserModel(AbstractUser):
    username        = None
    email           = models.EmailField(verbose_name="Email", unique=True, max_length=255)
    name            = models.CharField(verbose_name="Name", max_length=255, null=True, blank=True)
    role            = models.CharField(verbose_name="Role", choices=ROLE,max_length=255, null=True, blank=True)
    objects         = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]


    def __str__(self):
        return str(self.email)
