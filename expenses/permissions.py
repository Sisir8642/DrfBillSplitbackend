
from rest_framework.permissions import BasePermission 
from groups.models import GroupMember

class IsGroupMember(BasePermission):
    def has_permission(self, request, view):
        group_id = request.data.get('group') or request.query_params.get('group')
        if group_id and request.user.is_authenticated:
            return GroupMember.objects.filter(group_id=group_id, user=request.user).exists()
        return False