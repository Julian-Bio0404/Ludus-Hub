"""Tournament document serializers."""

from apps.search.documents import TournamentDocument
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer


class TournamentDocumentSerializer(DocumentSerializer):
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
