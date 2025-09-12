import uuid
from django.db import models
from django.conf import settings
from groups.models import Group

class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_id= models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expenses")
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="paid_expenses")
    description = models.TextField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    SPLIT_CHOICES = [
        ('equal', 'Equal'),
        ('unequal', 'Unequal'),
        ('percentage', 'Percentage'),
    ]
    split_type = models.CharField(max_length=10, choices=SPLIT_CHOICES, default='equal')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"
