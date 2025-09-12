from django.db import models
from expenses.models import Expense
from django.conf import settings
from decimal import Decimal
import uuid

class ExpenseParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expense_shares")
    share_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))


    def __str__(self):
        return f"{self.user.email} owes {self.share_amount} for {self.expense.description}"

