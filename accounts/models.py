from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from .manager import CustomUserManager

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        unique=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_code = models.PositiveBigIntegerField(null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email    
    
