from rest_framework import generics, permissions
from .models import Group, GroupMember, Invitation
from .serializers import GroupSerializer, InvitationSerializer, GroupMemberSerializer, AcceptInvitationSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from activityLog.models import Activity
# Create your views here.

class GroupListView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return Group.objects.all()
        return Group.objects.filter(members__user= self.request.user)

    def perform_create(self, serializer):
        group=serializer.save(created_by=self.request.user)
        member=GroupMember.objects.create(user=self.request.user, group=group, email=self.request.user.email)
        print("Group member created:", member)
        
        Activity.objects.create(
                group=group,
                user=self.request.user,
                action="Created the group",
                metadata={"group_name": group.name}
            )

class GroupDetailView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'id'  
    permission_classes = [IsAuthenticated]

class GroupMemberListView(generics.ListAPIView):
    serializer_class=GroupMemberSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return GroupMember.objects.filter(group__id=group_id)

class InvitationSendView(generics.CreateAPIView):
     serializer_class = InvitationSerializer
    #   permission_classes = [permissions.IsAuthenticated]

    #  def perform_create(self, serializer):
    #      serializer.save(invited_by=self.request.user)

     def post(self, request):
         serializer= InvitationSerializer(data= request.data, context={'request': request})
         if(serializer.is_valid()):
             invite= serializer.save()

             frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
             link = f"{frontend_url}/accept-invite/{invite.token}/"
             send_mail(
                 subject="Group-Invitation",
                 message=f"You have been invited to join a group for settlements. Click the link to accept: {link}",
                 from_email=settings.EMAIL_HOST_USER,
                 recipient_list=[invite.email],
             )
             
             Activity.objects.create(
                group=invite.group,  
                user=request.user,  
                action=f"Sent invitation to {invite.email} for group '{invite.group.name}'",
                metadata={"invite_id": str(invite.id)}
            )
             return Response({"message": "Invitation sent!"}, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                   
     


class AcceptInvitationView(generics.GenericAPIView):
    serializer_class = AcceptInvitationSerializer 
    permission_classes=[IsAuthenticated]

    def get(self, request, token):
        try:
           invite=Invitation.objects.get(token=token, is_accepted=False)
        except Invitation.DoesNotExist:
            return Response({"error": "Invalid or expired invitation"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_authenticated:
            return Response({"error": "Login required to accept invitation"}, status=status.HTTP_401_UNAUTHORIZED)
        
        GroupMember.objects.get_or_create(
             email=invite.email,
             group=invite.group,
             user=request.user,
         )
        
        invite.is_accepted = True
        invite.save()
        
        Activity.objects.create(
            group=invite.group,
            user=request.user,
            action="Accepted an invitation",
            metadata={"invited_by": invite.invited_by.email, "group_name": invite.group.name}
        )
        
        return Response(
    {
        "message": "You have joined the group!",
        "group_id": str(invite.group.id),  
    },
    status=status.HTTP_200_OK
)

