# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.models import AbstractUser


# class User(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     email=models.EmailField(unique=True)
#     password = models.TextField(max_length=20)
#     created_at=models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username= models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email
