from django.urls import path
from .views import (
    ExpenseParticipantListCreateView
)

urlpatterns = [

    path('expenses/<uuid:expense_id>/participants/', ExpenseParticipantListCreateView.as_view(), name='expense-participants'),
]
