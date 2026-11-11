from django.contrib import admin
from .models import UserProfile, LoginLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'login_count', 'last_login_ip']
    readonly_fields = ['login_count', 'last_login_ip']

@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display  = ['user', 'timestamp', 'ip_address', 'success']
    list_filter   = ['success']
    readonly_fields = ['user', 'timestamp', 'ip_address', 'success', 'user_agent']
