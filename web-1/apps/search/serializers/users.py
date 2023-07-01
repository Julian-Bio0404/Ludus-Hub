"""User document serializers."""

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from apps.search.documents import UserDocument


class UserDocumentSerializer(DocumentSerializer):
    """User document serializer."""

    class Meta:
        """Meta options."""
        document = UserDocument
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'role'
            'profile'
        )
