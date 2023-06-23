"""Users model admin."""

from apps.users.models import Profile, Subscription, User
from django.contrib import admin

# Admin configurations
admin.site.site_header = 'Ludus Hub'


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
    suit_classes = 'suit-tab suit-tab-profile'


class SubscriptionInline(admin.StackedInline):
    """Subscription in-line admin for users."""

    model = Subscription
    readonly_fields = [
        'plan', 'active',
        'created', 'updated'
    ]

    can_delete = False
    verbose_name_plural = 'subscriptions'
    suit_classes = 'suit-tab suit-tab-subscription'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User model admin."""

    inlines = [ProfileInline, SubscriptionInline]

    list_display = [
        'pk', 'customer_id',
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

    fieldsets = (
        ('Details', {
            'classes': ('suit-tab', 'suit-tab-details'),
            'fields': (
                'first_name', 'last_name',
                'username',
            ),
        }),
        ('Contact', {
            'classes': ('suit-tab', 'suit-tab-contact'),
            'fields': (
                'email', 'phone_number',
            ),
        }),
        ('Status', {
            'classes': ('suit-tab', 'suit-tab-status'),
            'fields': (
                'role', 'verified',
            ),
        }),
    )

    suit_form_tabs = (
        ('details', 'Details'),
        ('contact', 'Contact'),
        ('status', 'Status'),
        ('profile', 'Profile'),
        ('subscription', 'Subscription')
    )

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Subscription model admin."""

    list_display = ['user', 'plan', 'active']

    def has_change_permission(self, request, obj=None) -> bool:
        return False
