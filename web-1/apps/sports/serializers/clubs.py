"""Club serializers."""

from apps.sports.models import Club, Sport
from rest_framework import serializers


class ClubModelSerializer(serializers.ModelSerializer):
    """Club model serializer."""

    trainer = serializers.StringRelatedField(read_only=True)
    sport = serializers.CharField(required=False)

    class Meta:
        """Meta options."""
        model = Club
        fields = [
            'name', 'slug',
            'description', 'photo',
            'cover_photo', 'city',
            'trainer', 'web_site',
            'sport'
        ]

        read_only_fields = ['trainer']

    def validate(self, data):
        sport_name = data.get('sport')
        if sport_name:
            sport = Sport.objects.filter(name=sport_name).last()
            data.pop('sport')
            if sport:
                self.context['sport'] = sport
        return data

    def create(self, data):
        """Create a Club."""
        data['trainer'] = self.context['trainer']
        data['sport'] = self.context.get('sport')
        return Club.objects.create(**data)

    def update(self, instance, data):
        data['sport'] = self.context.get('sport')
        return super().update(instance, data)
