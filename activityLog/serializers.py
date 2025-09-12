from rest_framework import serializers
from activityLog.models import Activity

class ActivityLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Activity
        fields = ['id', 'group', 'user', 'action', 'metadata', 'created_at']
