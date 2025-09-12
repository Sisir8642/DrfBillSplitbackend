from rest_framework import serializers
from .models import Expense
from expenseparticipant.models import ExpenseParticipant
from expenseparticipant.serializers import ExpenseParticipantSerializer
from rest_framework import serializers 
from user.models import User

class ExpenseSerializer(serializers.ModelSerializer):
    participants= ExpenseParticipantSerializer(many=True)
    
    paid_by= serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='email',
        
    )
    class Meta:
        model= Expense
        fields= ['id', 'group_id', 'paid_by', 'description', 'amount', 'split_type', 'created_at', 'participants']
        read_only_fields =['created_at', 'id']

    def validate(self, data):
        split_type = data.get('split_type')
        participants = data.get('participants')
        total_amount = data.get('amount')

        if split_type == 'equal':
            return data
        elif split_type == 'unequal':
            total = sum(p['share_amount'] for p in participants)
            if total != total_amount:
                raise serializers.ValidationError("Total share amount must equal total expense amount for UNEQUAL split.")
        elif split_type == 'percentage':
            total = sum(p['share_amount'] for p in participants)
            if total != 100:
                raise serializers.ValidationError("Total percentage must be 100.")
        return data 
        


    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        split_type = validated_data.get('split_type')
        amount = validated_data.get('amount')

        expense = Expense.objects.create(**validated_data)

        if split_type == 'equal':
            share = round(amount / len(participants_data), 2)
            for p in participants_data:
                ExpenseParticipant.objects.create(
                    expense=expense,
                    user=p['user'],
                    share_amount=share,
                    paid_amount=p.get('paid_amount', 0)
                )
        elif split_type == 'unequal':
            for p in participants_data:
                ExpenseParticipant.objects.create(
                    expense=expense,
                    user=p['user'],
                    share_amount=p['share_amount'],
                    paid_amount=p.get('paid_amount', 0)
                )
        elif split_type == 'percentage':
            for p in participants_data:
                share_amt = round((p['share_amount'] / 100) * amount, 2)
                ExpenseParticipant.objects.create(
                    expense=expense,
                    user=p['user'],
                    share_amount=share_amt,
                    paid_amount=p.get('paid_amount', 0)
                )
        return expense

    
    def update(self, instance, validated_data):
        participants_data = validated_data.pop('participants', None)

        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if participants_data is not None:
            
            existing_participants = {p.user.email: p for p in instance.participants.all()}

            
            for p_data in participants_data:
                user = p_data['user']
                share_amount = p_data['share_amount']
                paid_amount = p_data.get('paid_amount', 0)

                if user.email in existing_participants:
                    participant = existing_participants.pop(user.email)
                    participant.share_amount = share_amount
                    participant.paid_amount = paid_amount
                    participant.save()
                else:
                    
                    ExpenseParticipant.objects.create(
                        expense=instance,
                        user=user,
                        share_amount=share_amount,
                        paid_amount=paid_amount
                    )

            
            for participant in existing_participants.values():
                participant.delete()

        return instance

        