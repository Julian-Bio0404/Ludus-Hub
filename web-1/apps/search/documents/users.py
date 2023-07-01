"""User documents."""

from django_elasticsearch_dsl import Document, fields
from apps.users.models import User, Profile
from django_elasticsearch_dsl.registries import registry


@registry.register_document
class UserDocument(Document):
    """User elasticsearch document."""

    profile = fields.ObjectField(properties={
        'photo': fields.FileField(),
        'cover_photo': fields.FileField(),
        'about': fields.TextField()
    })

    def get_queryset(self):
        """Improve performance we can select related in one sql request."""
        query = super(UserDocument, self).get_queryset().select_related('profile')
        return query

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Profile):
            return related_instance.user

    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = User
        related_models = (Profile,)
        fields = (
            'first_name',
            'last_name',
            'username',
            'role'
        )
