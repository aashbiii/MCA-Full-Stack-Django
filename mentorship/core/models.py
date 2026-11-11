from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [('mentor', 'Mentor'), ('mentee', 'Mentee')]
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role         = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio          = models.TextField(max_length=300, blank=True)
    phone        = models.CharField(max_length=20, blank=True)
    subject      = models.CharField(max_length=100, blank=True)
    avatar_color = models.CharField(max_length=20, default='#6366f1')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"

    def is_mentor(self):
        return self.role == 'mentor'

    def is_mentee(self):
        return self.role == 'mentee'


class Meeting(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('accepted',  'Accepted'),
        ('declined',  'Declined'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    REQUESTER_CHOICES = [('mentor', 'Mentor'), ('mentee', 'Mentee')]

    mentor       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_meetings')
    mentee       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_meetings')
    title        = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    meeting_date = models.DateTimeField()
    status       = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    requested_by = models.CharField(max_length=10, choices=REQUESTER_CHOICES)
    notes        = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-meeting_date']

    def __str__(self):
        return f"{self.title} ({self.mentor.username} ↔ {self.mentee.username})"

    def is_past(self):
        from django.utils import timezone
        return self.meeting_date < timezone.now()
