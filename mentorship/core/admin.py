from django.contrib import admin
from .models import Profile, Meeting

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'role', 'subject', 'phone']
    list_filter   = ['role']

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display  = ['title', 'mentor', 'mentee', 'meeting_date', 'status', 'requested_by']
    list_filter   = ['status', 'requested_by']
    search_fields = ['title', 'mentor__username', 'mentee__username']
