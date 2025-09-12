from rest_framework import generics, permissions
from .models import Activity
from .serializers import ActivityLogSerializer

class ActivityLogListView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        return Activity.objects.filter(group_id=group_id)
