from django.urls import path
from .views import GroupListView, GroupMemberListView,InvitationSendView,AcceptInvitationView,GroupDetailView

urlpatterns = [
    path('', GroupListView.as_view(), name='group-list-create'),
    path('<uuid:group_id>/members/', GroupMemberListView.as_view(), name='group-members'),
    path('groups/<uuid:group_id>/members/', GroupMemberListView.as_view(), name='group-members-alias'), 
    path('<uuid:id>/', GroupDetailView.as_view(), name='group-detail'),
    path('invite/', InvitationSendView.as_view(), name='send-invite'),
    path('accept-invite/<uuid:token>/', AcceptInvitationView.as_view(), name='accept-invite'),
]