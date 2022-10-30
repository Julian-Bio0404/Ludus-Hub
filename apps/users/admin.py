"""Users model admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from apps.users.models import Profile, User


class ProfileInline(admin.StackedInline):
    """Profile in-line admin for users."""

    model = Profile
    readonly_fields = [
        'photo', 'cover_photo',
        'about', 'birth_date',
        'sport', 'country',
        'public', 'web_site',
        'social_link'
    ]

    can_delete = False
    verbose_name_plural = 'profile'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User model admin."""

    inlines = [ProfileInline]

    list_display = [
        'pk',
        'first_name', 'last_name',
        'username', 'email',
        'phone_number', 'role',
        'verified', 'created', 'updated'
    ]

    list_display_links = ['pk', 'username']

    search_fields = [
        'username', 'email',
        'first_name', 'last_name'
    ]

    list_filter = ['verified', 'role']
    ordering = ['first_name', 'last_name']

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
