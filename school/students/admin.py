# Q22 — Register Student model in Django Admin panel
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display   = ('roll_no', 'name', 'branch', 'year', 'email', 'phone')
    list_filter    = ('branch', 'year')
    search_fields  = ('name', 'roll_no', 'email')
    ordering       = ('roll_no',)
