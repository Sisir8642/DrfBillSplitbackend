from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import ExpenseParticipantSerializer
from .models import ExpenseParticipant

# Create your views here.
class ExpenseParticipantListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        expense_id = self.kwargs.get('expense_id')
        return ExpenseParticipant.objects.filter(expense_id=expense_id)

    def perform_create(self, serializer):
        expense_id = self.kwargs.get('expense_id')
        serializer.save(expense_id=expense_id)