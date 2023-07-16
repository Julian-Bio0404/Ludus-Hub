"""Tournment documents."""

from apps.sports.models import Sport, Tournament
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class TournamentDocument(Document):
    """Tournament elasticsearch document."""

    name = fields.KeywordField()
    type = fields.KeywordField()
    city = fields.KeywordField()
    level = fields.KeywordField()

    sport = fields.ObjectField(
        properties={
            'name': fields.KeywordField(),
            'slug': fields.TextField(),
            'icon': fields.FileField()
        }
    )

    def get_queryset(self):
        """Improve performance we can select related in one sql request."""
        query = super(TournamentDocument, self).get_queryset()
        return query.select_related('sport')

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Sport):
            return related_instance.tournament_set.all()

    class Index:
        name = 'tournaments'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Tournament
        related_models = (Sport,)
        fields = (
            'id',
            'created',
            'updated'
        )
