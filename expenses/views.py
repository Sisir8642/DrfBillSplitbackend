from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import ExpenseSerializer
from .permissions import IsGroupMember
from rest_framework import status
from .models import Expense
from activityLog.models import Activity
# Create your views here.
class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class=ExpenseSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        if(group_id := self.request.query_params.get('group')):    
            return Expense.objects.filter(group_id=group_id)
        return Expense.objects.all() 
    
    def perform_create(self, serializer):
        serializer.save(paid_by=self.request.user)
        expense = serializer.save()
        Activity.objects.create(
            group=expense.group_id,
                user=expense.paid_by,
                action="Added a new expense",
                metadata={
                    "description": expense.description,
                    "amount": str(expense.amount),
                    "split_type": expense.split_type
                }
        )


class ExpenseDetailView(generics.RetrieveAPIView):
    queryset= Expense.objects.all()
    serializer_class= ExpenseSerializer
    permission_classes=[IsGroupMember]
