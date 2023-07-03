"""User document serializers."""

from apps.search.documents import UserDocument
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers


class UserDocumentSerializer(DocumentSerializer):
    """User document serializer."""

    profile = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    def get_profile(self, obj):
        """Serialize user profile."""
        return obj.profile.to_dict()

    def get_role(self, obj):
        """Get user role."""
        return obj.role

    class Meta:
        """Meta options."""
        document = UserDocument
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'role'
            'profile',
            'created',
            'updated'
        )
