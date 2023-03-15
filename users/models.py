from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name=None, last_name=None, email=None, avatar = None, phone_number=None, password=None,**extra_fields):
        if not password:
            raise ValueError('The password must be set')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, avatar=avatar, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name=None, last_name=None, email=None, avatar = None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(first_name=first_name, last_name=last_name, email=email, avatar=avatar, phone_number=phone_number, password=password,**extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    is_host = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'password']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.first_name:
            raise ValueError('The First Name field must be set')
        if not self.last_name:
            raise ValueError('The Last Name field must be set')
        if not self.phone_number:
            raise ValueError('The Phone Number field must be set')
        if not self.email:
            raise ValueError('The Email field must be set')

        super().save(*args, **kwargs)
