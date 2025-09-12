from django.contrib import admin
from activityLog.models import Activity 

@admin.register(Activity)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'action', 'created_at')
    list_filter = ('group', 'action', 'created_at')
    search_fields = ('user__username', 'action')
    ordering = ('-created_at',)