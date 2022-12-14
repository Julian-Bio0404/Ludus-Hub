"""Club serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from apps.sports.models import Club


class ClubModelSerializer(serializers.ModelSerializer):
    """Club model serializer."""

    trainer = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options."""
        model = Club
        fields = [
            'name', 'slug',
            'description', 'photo',
            'cover_photo', 'city',
            'trainer', 'web_site'
        ]

        read_only_fields = ['trainer', 'slug']

    def create(self, data):
        """Create a Club."""
        trainer = self.context['trainer']
        return Club.objects.create(**data, trainer=trainer)
