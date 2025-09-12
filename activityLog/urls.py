from django.urls import path
from .views import ActivityLogListView

urlpatterns = [
    path('groups/<uuid:group_id>/activity-logs/', ActivityLogListView.as_view(), name='activity-log-list'),
]
