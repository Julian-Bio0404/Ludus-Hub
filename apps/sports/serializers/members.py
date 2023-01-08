"""Members serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.sports.models import Member, Invitation, Assistance
from apps.users.models import User

# Serializers
from apps.users.serializers import UserModelSerializer
from .clubs import ClubModelSerializer


class MemberModelSerializer(serializers.ModelSerializer):
    """Member model serializer."""

    user = UserModelSerializer(read_only=True)
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        model = Member
        fields = [
            'user', 'active',
            'joined_at'
        ]

        read_only_fields = ['user', 'joined_at']


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
        members = club.members.filter(user__username__in=members, active=True)
        if not members:
            raise serializers.ValidationError(
                'There are no existing members for this club.')
        self.context['members'] = members
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
