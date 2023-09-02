"""Sports models admin."""

import nested_admin
from apps.sports.models import (Assistance, Category, Club, Competitor, Draw,
                                Group, GroupMatch, Invitation, Match, Member,
                                Modality, Round, RoundGroup, RoundMatch, Rule,
                                Sport, Tag, Team, Tournament)
from apps.utils.admin import (BaseNestedTabularInline, BaseTabularInline,
                              ImageAdminMixin)
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_json_widget.widgets import JSONEditorWidget
from taskapp.tasks import create_sport_rules


class TeamMemberInline(BaseTabularInline):
    """Team member inline admin."""

    model = Team.users.through
    can_delete = False
    verbose_name_plural = 'Team members'
    suit_classes = 'suit-tab suit-tab-members'

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


class MemberInline(BaseTabularInline):
    """Club member inline admin."""

    model = Member
    # readonly_fields = ['user', 'active']
    can_delete = False
    verbose_name_plural = 'members'
    suit_classes = 'suit-tab suit-tab-members'

    def has_add_permission(self, request, obj=None) -> bool:
        return False


class TeamInline(BaseTabularInline):
    """Team inline admin."""

    model = Team
    readonly_fields = ['club', 'category', 'team_name']
    can_delete = False
    verbose_name_plural = 'teams'
    fields = ['team_name', 'category']
    suit_classes = 'suit-tab suit-tab-teams'

    def team_name(self, obj):
        if obj.pk:
            url = reverse('admin:sports_team_change', args=[obj.pk])
            return mark_safe('<a href="{}">{}</a>'.format(url, obj.name))
        return '-'

    team_name.short_description = 'Name'
    team_name.allow_tags = True

    def has_add_permission(self, request, obj=None) -> bool:
        return False


class InvitationInline(BaseTabularInline):
    """Club invitation inline admin."""

    model = Invitation
    readonly_fields = ['sent_by', 'invited', 'used']
    can_delete = False
    verbose_name_plural = 'invitations'
    suit_classes = 'suit-tab suit-tab-invitations'

    def has_add_permission(self, request, obj=None) -> bool:
        return False


class AssistanceInline(BaseTabularInline):
    """Club assistance inline admin."""

    model = Assistance
    readonly_fields = ['user', 'club']
    can_delete = False
    verbose_name_plural = 'assistances'
    suit_classes = 'suit-tab suit-tab-assistances'

    def has_add_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin, ImageAdminMixin):
    """Club model admin."""

    list_display = [
        'name', 'slug',
        'description', 'city',
        'trainer', 'web_site',
        'photo_preview', 'cover_photo_preview',
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

    fieldsets = (
        ('Details', {
            'classes': ('suit-tab', 'suit-tab-details'),
            'fields': (
                'name', 'slug', 'sport', 'description',
                'city', 'trainer', 'web_site',
                'photo', 'cover_photo',
            ),
        }),
    )

    suit_form_tabs = (
        ('details', 'Details'),
        ('members', 'Members'),
        ('teams', 'Teams'),
        ('invitations', 'Invitations'),
        ('assistances', 'Assistances')
    )

    # def has_add_permission(self, request, obj=None) -> bool:
    #     return False

    # def has_delete_permission(self, request, obj=None) -> bool:
    #     return False

    # def has_change_permission(self, request, obj=None) -> bool:
    #     return False


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

    fieldsets = (
        ('Details', {
            'classes': ('suit-tab', 'suit-tab-details'),
            'fields': ('name', 'club', 'category'),
        }),
    )

    suit_form_tabs = (
        ('details', 'Details'),
        ('members', 'Members')
    )

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


class CategoryInline(BaseTabularInline):
    """Category inline admin."""

    model = Sport.categories.through
    suit_classes = 'suit-tab suit-tab-categories'
    verbose_name_plural = 'Categories'


class TagInline(BaseTabularInline):
    """Tag inline admin."""

    model = Sport.tags.through
    suit_classes = 'suit-tab suit-tab-tags'
    verbose_name_plural = 'Tags'


class RuleInline(BaseTabularInline):
    """Sport Rules inline."""

    model = Rule
    suit_classes = 'suit-tab suit-tab-rules'

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget(mode='tree')}
    }


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
        'type', 'created'
    ]

    search_fields = ['name']

    list_filter = ['modality', 'gender', 'type']

    fieldsets = (
        None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('modality', 'gender', 'name', 'type'),
        }),


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin, ImageAdminMixin):
    """Sport model admin."""

    list_display = [
        'name', 'slug',
        'icon_preview', 'created',
        'updated'
    ]

    search_fields = ['name']

    inlines = [RuleInline, CategoryInline, TagInline]

    fieldsets = (
        'Details', {
            'classes': ('suit-tab', 'suit-tab-details'),
            'fields': ('name', 'icon', 'description'),
        }),

    suit_form_tabs = (
        ('details', 'Details'),
        ('rules', 'Rules'),
        ('categories', 'Categories'),
        ('tags', 'Tags'),
    )

    def save_formset(self, request, form, formset, change):
        if formset.prefix == 'Sport_categories':
            sport = form.instance
            removed_modality_ids = []
            added_modality_ids = []
            for form_obj in formset.forms:
                data = form_obj.cleaned_data
                category = data.get('category')
                if data.get('DELETE', False):
                    removed_modality_ids.append(category.modality.id)
                else:
                    added_modality_ids.append(category.modality.id)

            if removed_modality_ids:
                kwargs = {
                    'id': sport.id,
                    'modality_ids': removed_modality_ids,
                    'action': 'remove'
                }
            elif added_modality_ids:
                kwargs = {
                    'id': sport.id,
                    'modality_ids': added_modality_ids,
                    'action': 'add'
                }

            if removed_modality_ids or added_modality_ids:
                create_sport_rules.delay(**kwargs)
        return super().save_formset(request, form, formset, change)


class TournamentCategoryInline(BaseNestedTabularInline):
    """Category inline admin."""

    model = Tournament.categories.through
    suit_classes = 'suit-tab suit-tab-categories'
    verbose_name = 'Category'
    verbose_name_plural = 'Categories'


class RefereesInline(BaseNestedTabularInline):
    """Referees inline."""

    model = Tournament.referees.through
    verbose_name_plural = 'Referees'
    suit_classes = 'suit-tab suit-tab-referees'


class RefereeInvitations(BaseNestedTabularInline):
    """Referee invitation inine admin."""

    model = Tournament.referee_invitations.through
    verbose_name_plural = 'Referee invitations'
    suit_classes = 'suit-tab suit-tab-referee-invitations'


class BaseCompetitorInline(BaseNestedTabularInline):
    """Base competitor inline admin."""

    verbose_name_plural = 'Competitors'


class CompetitorInline(BaseCompetitorInline):
    """Competitor inline admin"""

    model = Competitor
    suit_classes = 'suit-tab suit-tab-competitors'


class CompetitorsInline(BaseCompetitorInline):
    """
    Competitors inline admin.
    Util for Match admin that have a relation many to many
    with competitors.
    """

    model = Match.competitors.through
    readonly_fields = ['rating']

    def rating(self, obj):
        if obj.pk:
            return obj.rating.score
        return '-'
    rating.short_description = 'Score'
    rating.allow_tags = True


class GroupMatchInline(BaseNestedTabularInline):
    """Group Match inline admin."""

    model = GroupMatch
    verbose_name_plural = 'Matches Group'


class RoundMatchInline(BaseNestedTabularInline):
    """Round Match inline admin."""

    model = RoundMatch
    verbose_name_plural = 'Matches'
    readonly_fields = ['clash']

    def clash(self, obj):
        if obj.pk:
            url = reverse('admin:sports_match_change', args=[obj.match.pk])
            return mark_safe('<a href="{}">{}</a>'.format(url, obj.match))
        return '-'
    clash.short_description = 'Match Link'
    clash.allow_tags = True


class RoundGroupInline(BaseNestedTabularInline):
    """Round Group inline admin."""

    model = RoundGroup
    verbose_name_plural = 'Matches Groups'
    readonly_fields = ['group_matches']

    def group_matches(self, obj):
        if obj.pk:
            url = reverse('admin:sports_group_change', args=[obj.group.pk])
            return mark_safe('<a href="{}">{}</a>'.format(url, obj.group))
        return '-'

    group_matches.short_description = 'Match Group Link'
    group_matches.allow_tags = True


class RoundInline(BaseNestedTabularInline):
    """Round inline admin."""

    model = Round
    verbose_name_plural = 'Rounds'
    inlines = [RoundMatchInline, RoundGroupInline]


class DrawInline(BaseNestedTabularInline):
    """Draw inline admin"""

    model = Draw
    verbose_name_plural = 'Draws'
    suit_classes = 'suit-tab suit-tab-draws'
    inlines = [RoundInline]


class AdministratorInline(BaseNestedTabularInline):
    """Administrator inline admin."""

    model = Tournament.administrators.through
    verbose_name_plural = 'Administrators'
    suit_classes = 'suit-tab suit-tab-administrators'


@admin.register(Tournament)
class TournamentAdmin(nested_admin.NestedModelAdmin):
    """Tournament model admin."""

    list_display = ['name', 'slug', 'type', 'level', 'created', 'updated']

    search_fields = ['name']

    list_filter = ['type', 'level']

    inlines = [
        TournamentCategoryInline,
        RefereesInline,
        RefereeInvitations,
        AdministratorInline,
        CompetitorInline,
        DrawInline
    ]

    fieldsets = (
        ('Details', {
            'classes': ('suit-tab', 'suit-tab-details'),
            'fields': (
                'name', 'type',
                'level', 'sport',
                'description', 'date',
                'city', 'address'
            ),
        }),
    )

    suit_form_tabs = (
        ('details', 'Details'),
        ('categories', 'Categories'),
        ('referees', 'Referees'),
        ('referee-invitations', 'Referee Invitations'),
        ('administrators', 'Administrators'),
        ('competitors', 'Competitors'),
        ('draws', 'Draws'),
    )


@admin.register(Match)
class MatchAdmin(nested_admin.NestedModelAdmin):
    """Match admin."""

    list_display = ['title', 'type', 'state', 'created', 'updated']

    list_filter = ['type', 'state']

    inlines = [CompetitorsInline]


@admin.register(Group)
class GroupAdmin(nested_admin.NestedModelAdmin):
    """Group admin."""

    list_display = ['title', 'created', 'updated']

    inlines = [GroupMatchInline]
