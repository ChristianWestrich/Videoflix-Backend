from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
# Create your models here.
class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email