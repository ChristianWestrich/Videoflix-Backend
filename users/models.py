from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
# Create your models here.
class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.email