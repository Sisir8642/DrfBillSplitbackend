import uuid
from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group
from expenses.models import Expense
User = get_user_model()

class Settlement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='settlements')
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lent_settlements') 
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_settlements')  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('group', 'lender', 'borrower')


    def __str__(self):
        return f"{self.borrower} owes {self.lender} {self.amount} in {self.group}"
