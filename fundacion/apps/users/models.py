from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        app_label = 'users'
