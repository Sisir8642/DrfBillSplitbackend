from rest_framework import serializers
from django.db import models
from expenseparticipant.models import ExpenseParticipant
from user.models import User
from decimal import Decimal


class ExpenseParticipantSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='email'  
    )
    share_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), required=False)

    class Meta:
        model = ExpenseParticipant
        fields = [ 'user', 'share_amount', 'paid_amount']
   
 