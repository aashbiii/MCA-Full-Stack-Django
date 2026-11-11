from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_ADMIN   = 'admin'
    ROLE_TEACHER = 'teacher'
    ROLE_STUDENT = 'student'
    ROLE_CHOICES = [
        ('admin',   'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone      = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username + ' (' + self.get_role_display() + ')'

    def is_admin_role(self):    return self.role == 'admin'
    def is_teacher_role(self):  return self.role == 'teacher'
    def is_student_role(self):  return self.role == 'student'
