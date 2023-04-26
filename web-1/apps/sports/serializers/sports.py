"""Sport serializers."""

from rest_framework import serializers
from apps.sports.models import Sport


class SportModelSerializer(serializers.ModelSerializer):
    """Sport model serializer."""

    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        return [c.__str__() for c in obj.categories.all()]

    class Meta:
        """Meta options."""
        model = Sport
        fields = [
            'id', 'name', 'slug',
            'description', 'icon',
            'categories'
        ]
