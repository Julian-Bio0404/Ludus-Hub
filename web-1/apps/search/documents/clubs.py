"""Club documents."""

from apps.sports.models import Club, Sport
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class ClubDocument(Document):
    """Club elasticsearch document."""

    name = fields.KeywordField()

    sport = fields.ObjectField(
        properties={
            'id': fields.KeywordField(),
            'name': fields.KeywordField(),
            'slug': fields.TextField(),
            'icon': fields.FileField()
        }
    )

    def get_queryset(self):
        """Improve performance we can select related in one sql request."""
        query = super(ClubDocument, self).get_queryset().select_related('sport')
        return query

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Sport):
            return related_instance.club_set.all()

    class Index:
        name = 'clubs'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Club
        related_models = (Sport,)
        fields = (
            'id',
            'slug',
            'photo',
            'cover_photo',
            'city',
            'created',
            'updated'
        )
