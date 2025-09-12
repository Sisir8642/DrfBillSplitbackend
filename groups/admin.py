from django.contrib import admin
from .models import Group, GroupMember, Invitation
# Register your models here.
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Invitation)