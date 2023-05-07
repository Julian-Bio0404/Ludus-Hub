"""Sports models admin."""

from apps.sports.models import (Assistance, Category, Club, Invitation, Member,
                                Modality, Sport, Tag, Team)
from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe


class TeamMemberInline(admin.TabularInline):
    """Team member inline admin."""

    model = Team.users.through
    suit_form_inlines_hide_original = True
    extra = 0
    can_delete = False
    verbose_name_plural = 'Team members'

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


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


class TeamInline(admin.TabularInline):
    """Team inline admin."""

    model = Team
    suit_form_inlines_hide_original = True
    readonly_fields = ['club', 'category', 'team_name']
    extra = 0
    can_delete = False
    verbose_name_plural = 'teams'
    fields = ['team_name', 'category']

    def team_name(self, obj):
        if obj.pk:
            url = reverse('admin:sports_team_change', args=[obj.pk])
            return mark_safe('<a href="{}">{}</a>'.format(url, obj.name))
        return '-'
    team_name.short_description = 'Name'
    team_name.allow_tags = True

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

    inlines = [
        MemberInline,
        TeamInline,
        InvitationInline,
        AssistanceInline
    ]

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Team model admin."""

    list_display = [
        'name', 'slug',
        'club', 'category',
        'created', 'updated'
    ]

    search_fields = ['name', 'slug']

    inlines = [TeamMemberInline]

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


class SportForm(forms.ModelForm):
    """Sport form admin."""

    class Meta:
        model = Sport
        exclude = ('categories', 'tags')


class CategoryInline(admin.TabularInline):
    """Category inline admin."""

    model = Sport.categories.through
    extra = 0
    verbose_name_plural = 'Categories'
    suit_form_inlines_hide_original = True


class TagInline(admin.TabularInline):
    """Tag inline admin."""

    model = Sport.tags.through
    extra = 0
    verbose_name_plural = 'Tags'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag Admin."""

    list_display = [
        'name', 'slug',
        'created', 'updated'
    ]

    search_fields = ['name']


@admin.register(Modality)
class ModalityAdmin(admin.ModelAdmin):
    """Modality Admin."""

    list_display = [
        'name', 'slug',
        'created', 'updated'
    ]

    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin."""

    list_display = [
        'name', 'slug',
        'modality', 'gender',
        'created'
    ]

    search_fields = ['name']

    list_filter = ['modality', 'gender']

    fieldsets = (
        None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('modality', 'gender', 'name'),
        }),


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    """Sport model admin."""

    form = SportForm

    list_display = [
        'name', 'slug',
        'icon', 'created',
        'updated'
    ]

    search_fields = ['name']

    inlines = [CategoryInline, TagInline]

    fieldsets = (
        'Details', {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('name', 'icon', 'description'),
        }),
