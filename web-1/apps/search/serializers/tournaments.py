"""Tournament document serializers."""

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from apps.search.documents import TournamentDocument


class ClubDocumentSerializer(DocumentSerializer):
    """Tournament document Serializer."""

    class Meta:
        """Meta options."""
        document = TournamentDocument
        fields = (
            'id',
            'name',
            'slug',
            'type',
            'level',
            'city',
            'sport'
        )
