"""Sports models admin."""

# Django
from django.contrib import admin

# Models
from apps.sports.models import Assistance, Club, Member, Invitation


class MemberInline(admin.TabularInline):
    """Club member inline admin."""

    model = Member
    suit_form_inlines_hide_original = True
    readonly_fields = ['user', 'active']
    extra = 0
    can_delete = False
    verbose_name_plural = 'members'

    def has_add_permission(self, request, obj=None) -> bool:
        return False


class InvitationInline(admin.TabularInline):
    """Club invitation inline admin."""

    model = Invitation
    suit_form_inlines_hide_original = True
    readonly_fields = ['sent_by', 'invited', 'used']
    extra = 0
    can_delete = False
    verbose_name_plural = 'invitations'

    def has_add_permission(self, request, obj=None) -> bool:
        return False


class AssistanceInline(admin.TabularInline):
    """Club assistance inline admin."""

    model = Assistance
    suit_form_inlines_hide_original = True
    readonly_fields = ['user', 'club']
    extra = 0
    can_delete = False
    verbose_name_plural = 'assistances'

    def has_add_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Club model admin."""

    list_display = [
        'name', 'slug',
        'description', 'city',
        'trainer', 'web_site',
        'created', 'updated'
    ]

    search_fields = [
        'name', 'slug', 'city'
    ]

    inlines = [MemberInline, InvitationInline, AssistanceInline]

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
