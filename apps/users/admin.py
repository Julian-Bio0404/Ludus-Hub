"""Users model admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from apps.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = [
        'pk',
        'first_name', 'last_name',
        'username', 'email',
        'phone_number', 'role',
        'verified', 'created', 'updated'
    ]

    list_display_links = ['pk', 'username']

    readonly_fields = [
        'pk',
        'first_name', 'last_name',
        'username', 'email',
        'phone_number', 'role',
        'created', 'updated'
    ]

    search_fields = [
        'username', 'email',
        'first_name', 'last_name',
        'verified'
    ]

    list_filter = ['verified', 'role']
    ordering = ['first_name', 'last_name']

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
