from rest_framework import serializers
from .models import Group, GroupMember, Invitation
from expenses.models import Expense
from expenseparticipant.models import ExpenseParticipant
from user.serializers import UserSerializer

class GroupSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True) 


    class Meta:
        model=Group
        fields = ['id', 'name', 'description', 'created_at', 'created_by']
        read_only_fields= ['created_at', 'created_by']


    def create(self, validated_data):
        user= self.context['request'].user
        validated_data.pop('created_by', None) 
        group= Group.objects.create(created_by=user, **validated_data)
        return group


class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model=GroupMember
        fields = ['id', 'email', 'group_id', 'user', 'joined_at']
        read_only_fields=['group_id', 'joined_at']
        
    def get_username(self, obj):
        return obj.user.username if obj.user else obj.email 
    
    def get_user_id(self, obj):
        return obj.user.id if obj.user else None

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Invitation
        fields=['id', 'email', 'group', 'token', 'invited_by', 'is_accepted', 'created_at']
        read_only_fields=['invited_by', 'token', 'is_accepted', 'created_at']

    def create(self, validated_data):
        user=self.context['request'].user
        return Invitation.objects.create(invited_by=user, **validated_data)
        


class AcceptInvitationSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)



    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        expense = Expense.objects.create(**validated_data)
        for participant_data in participants_data:
            ExpenseParticipant.objects.create(expense=expense, **participant_data)
        return expense
