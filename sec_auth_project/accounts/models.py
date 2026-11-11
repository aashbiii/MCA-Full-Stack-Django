from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio        = models.TextField(max_length=200, blank=True)
    avatar_initial = models.CharField(max_length=2, blank=True)
    login_count    = models.PositiveIntegerField(default=0)
    last_login_ip  = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class LoginLog(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_logs')
    timestamp  = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    success    = models.BooleanField(default=True)
    user_agent = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        status = "✓" if self.success else "✗"
        return f"{status} {self.user.username} @ {self.timestamp}"
