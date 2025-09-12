from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from groups.models import Group
from .utils import calculate_settlements_for_group

class RecalculateSettlementView(APIView):
    def post(self, request, group_id):
        group = Group.objects.get(id=group_id)
        settlements = calculate_settlements_for_group(group)
        return Response({"settlements": settlements})
