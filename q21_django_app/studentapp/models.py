from django.db import models

class Student(models.Model):
    name    = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    branch  = models.CharField(max_length=50)
    year    = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.roll_no})"

    class Meta:
        ordering = ['roll_no']
