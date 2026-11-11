# Q22 — Student Model (used for migrations & admin registration)
from django.db import models

BRANCH_CHOICES = [
    ('CSE', 'Computer Science'),
    ('ECE', 'Electronics'),
    ('ME',  'Mechanical'),
    ('CE',  'Civil'),
]

class Student(models.Model):
    name     = models.CharField(max_length=100)
    roll_no  = models.CharField(max_length=20, unique=True)
    branch   = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    year     = models.IntegerField()
    email    = models.EmailField(blank=True)
    phone    = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.name} ({self.roll_no})"

    class Meta:
        ordering = ['roll_no']
