"""Club document serializers."""

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from apps.search.documents import ClubDocument


class ClubDocumentSerializer(DocumentSerializer):
    """Club document Serializer."""

    class Meta:
        """Meta options."""
        document = ClubDocument
        fields = (
            'id',
            'name',
            'slug',
            'photo',
            'cover_photo',
            'city',
            'sport'
        )
