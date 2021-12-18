"""Users model admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from app.users.models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """User model admin."""

    list_display = [
        'pk', 'first_name', 
        'last_name', 'email', 
        'username', 'phone_number', 
        'verified',
        'created', 'updated'
    ]

    search_fields = [
        'username', 'email', 
        'first_name', 'last_name',
        'verified'
    ]

    list_filter = ['verified']
    ordering = ['first_name', 'last_name']