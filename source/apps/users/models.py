from django.db import models
from django.contrib.auth.models import AbstractUser
    
class User(AbstractUser):
    
    username = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=200, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name or self.username