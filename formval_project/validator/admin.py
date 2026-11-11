from django.contrib import admin
from .models import Registration

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display  = ['username', 'first_name', 'last_name', 'email', 'age', 'created_at']
    search_fields = ['username', 'email']
