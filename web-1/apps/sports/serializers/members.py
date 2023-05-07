"""Members serializers."""

from apps.sports.models import Assistance, Invitation, Member, Team
from apps.users.models import User
from apps.users.serializers import UserModelSerializer
from rest_framework import serializers

from .clubs import ClubModelSerializer


class MemberModelSerializer(serializers.ModelSerializer):
    """Member model serializer."""

    user = UserModelSerializer(read_only=True)
    joined_at = serializers.DateTimeField(source='created', read_only=True)
    assistances = serializers.IntegerField(source='all_assistances')

    class Meta:
        model = Member
        fields = [
            'user', 'active',
            'joined_at', 'assistances'
        ]

        read_only_fields = [
            'user', 'joined_at',
            'assistances'
        ]


class InvitationModelSerializer(serializers.ModelSerializer):
    """Invitation model serializer."""

    sent_by = UserModelSerializer(read_only=True)
    invited = UserModelSerializer(read_only=True)
    club = ClubModelSerializer(read_only=True)
    used = serializers.BooleanField()

    class Meta:
        model = Invitation
        fields = [
            'id', 'sent_by', 'invited',
            'club', 'used', 'created'
        ]

        read_only_fields = [
            'sent_by', 'invited',
            'club', 'created'
        ]


class CreateInvitationSerializer(serializers.Serializer):
    """Create Invitation serializer."""

    invited = serializers.CharField()

    def validate(self, data):
        """Verify that invited exists."""
        username = data['invited']
        try:
            invited = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                f'The user with username {username} does not exist')

        invitation = Invitation.objects.filter(
            invited=invited, club=self.context['club'])
        if invitation.exists():
            raise serializers.ValidationError(
                'This user already has a invitation for this club.')

        self.context['invited'] = invited
        return data

    def create(self, data):
        """Create a invitation."""
        sent_by = self.context['sent_by']
        invited = self.context['invited']
        club = self.context['club']
        invitation = Invitation.objects.create(
            sent_by=sent_by, invited=invited, club=club)

        # Create a inactive Membership
        Member.objects.create(user=invited, club=club)
        return invitation


class AssistanceModelSerializer(serializers.ModelSerializer):
    """Assistance model serializer."""

    user = UserModelSerializer(read_only=True)

    class Meta:
        model = Assistance
        fields = ['user', 'created']
        read_only_fields = ['user', 'created']


class CreateAssistanceSerializer(serializers.Serializer):
    """Create assistance serializer."""

    members = serializers.ListField(child=serializers.CharField())

    def validate(self, data):
        """Search members by club."""
        club = self.context['club']
        members = data['members']
        members = club.member_set.filter(
            user__username__in=members, active=True).select_related('user')
        if not members:
            raise serializers.ValidationError(
                'There are no existing members for this club.')
        self.context['members'] = [member.user for member in members]
        return data

    def create(self, data):
        """Assistances Bulk create."""
        query = [
            Assistance(
                user=member,
                club=self.context['club']
            ) for member in self.context['members']
        ]
        return Assistance.objects.bulk_create(query)


class BaseTeamMemberSerializer(serializers.Serializer):
    """Base Team Member serializer."""

    users = serializers.ListField(child=serializers.CharField())

    def validate_users(self, data):
        """Check members by club."""
        club = self.context['club']

        members = club.member_set.filter(
            user__username__in=data, active=True).select_related('user')

        if not members:
            raise serializers.ValidationError(
                'Select only active members for this club.')

        self.context['users'] = [member.user for member in members]
        return data


class TeamModelSerializer(serializers.ModelSerializer):
    """Team model serializer."""

    users = UserModelSerializer(many=True)
    category_id = serializers.UUIDField(required=False)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        category = obj.category
        return category.__str__() if category else None

    def to_representation(self, instance):
        """Exclude category_id from the serialized representation."""
        response = super().to_representation(instance)
        response.pop('category_id', None)
        return response

    def validate(self, data):
        club = self.instance.club
        sport = club.sport
        category_id = data.get('category_id')
        if sport and category_id:
            category = sport.categories.filter(id=category_id).last()
            if not category:
                raise serializers.ValidationError(
                    'The category does not exist for this club.')
            self.context['category'] = category
        return data

    def update(self, instance, data):
        category = self.context.get('category')
        if category:
            data['category'] = category
            data.pop('category_id', None)
        return super().update(instance, data)

    class Meta:
        model = Team
        fields = [
            'id', 'name',
            'slug', 'category',
            'category_id',
            'users', 'updated',
            'created'
        ]

        read_only_fields = ['club', 'slug', 'category']


class CreateTeamSerializer(serializers.Serializer):
    """Create Team serializer."""

    name = serializers.CharField()
    users = serializers.ListField(child=serializers.CharField(), required=False)
    category = serializers.UUIDField(required=False)

    def validate(self, data):
        """Check members by club and category."""
        club = self.context['club']
        usernames = data.get('users')
        category_id = data.get('category')
        sport = club.sport

        if usernames:
            members = club.member_set.filter(
                user__username__in=usernames, active=True).select_related('user')

            if not members:
                raise serializers.ValidationError(
                    'Select only active members for this club.')

            self.context['users'] = [member.user for member in members]
            data.pop('users')

        if not sport and category_id:
            raise serializers.ValidationError(
                    'Please, update the sport for this club.')

        if sport and category_id:
            category = sport.categories.filter(id=category_id).last()
            if not category:
                raise serializers.ValidationError(
                    'The category does not exist for this club.')
            self.context['category'] = category

        return data

    def create(self, data):
        """Create the team."""
        data['club'] = self.context['club']
        data['category'] = self.context.get('category')
        users = self.context.get('users')
        team = Team.objects.create(**data)
        # Set the users of the team
        if users:
            team.users.add(*users)
        return team


class AddTeamMemberSerializer(BaseTeamMemberSerializer):
    """Add Team Member serializer."""

    def save(self, **data):
        team = self.context['team']
        users = self.context['users']
        team.users.add(*users)
        return users


class RemoveTeamMemberSerializer(BaseTeamMemberSerializer):
    """Remove Team Member serializer."""

    def save(self, **data):
        team = self.context['team']
        users = self.context['users']
        team.users.remove(*users)
        return users
