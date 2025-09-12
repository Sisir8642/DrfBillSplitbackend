from django.urls import path
from .views import RecalculateSettlementView

urlpatterns = [
    path('groups/<uuid:group_id>/settlements/calculate/', RecalculateSettlementView.as_view(), name='group-settlement'),
]
