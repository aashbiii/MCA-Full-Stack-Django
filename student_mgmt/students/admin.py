from django.contrib import admin
from .models import Student, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'department', 'status', 'gpa']
    list_filter = ['status', 'department', 'gender']
    search_fields = ['student_id', 'first_name', 'last_name', 'email']
    date_hierarchy = 'enrollment_date'
