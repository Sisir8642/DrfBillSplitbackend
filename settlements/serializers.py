from rest_framework import serializers
from .models import Settlement
class SettlementSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')
    lender = serializers.CharField(source='lender.username')
    borrower = serializers.CharField(source='borrower.username')
    class Meta:
        model = Settlement
        fields = "__all__"

    def validate(self, data):
        amount = data.get('amount')
        if amount <= 0:
            raise serializers.ValidationError("Settlement amount must be greater than zero.")
        return data

    def create(self, validated_data):
        return Settlement.objects.create(**validated_data)