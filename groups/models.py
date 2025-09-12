from django.db import models
from user.models import User
from django.conf import settings

import uuid

# Create your models here.
class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name= models.CharField(max_length=50, null= False)
    # Group_avatar=models.ImageField()
    description= models.TextField(max_length=100, null=True, blank=True )
    created_at= models.DateTimeField(auto_now_add=True)
    created_by=  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group')

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # name= models.CharField(max_length=20)
    email = models.EmailField() 
    group= models.ForeignKey(Group, on_delete=models.CASCADE,related_name="members" )
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True 
    )
    joined_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} in {self.group_id}"




class Invitation(models.Model):
    email = models.EmailField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="invites")
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)










