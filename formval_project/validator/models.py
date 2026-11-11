from django.db import models

class Registration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    username   = models.CharField(max_length=30, unique=True)
    phone      = models.CharField(max_length=15)
    age        = models.IntegerField()
    website    = models.URLField(blank=True)
    bio        = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.email})"
