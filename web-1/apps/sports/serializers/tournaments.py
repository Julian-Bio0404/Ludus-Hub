"""Sport serializers."""

from rest_framework import serializers
from apps.sports.models import Tournament, Sport
from apps.sports.serializers import SportModelSerializer


class TournamentModelSerializer(serializers.ModelSerializer):
    """Tournament model serializer."""

    categories = serializers.SerializerMethodField()
    sport = SportModelSerializer

    def get_categories(self, obj):
        return [c.__str__() for c in obj.categories.all()]

    class Meta:
        """Meta options."""
        model = Tournament
        fields = [
            'id', 'name', 'slug',
            'type', 'level',
            'description', 'city',
            'address', 'sport'
            'date', 'categories',
            'referees', 'updated',
            'created'
        ]

    read_only_fields = ['sport', 'categories']


class CreateTournamentSerializer(serializers.Serializer):
    """Create Tournament serializer."""

    name = serializers.CharField(min_length=3)
    type = serializers.ChoiceField(choices=Tournament.Types.choices)
    level = serializers.ChoiceField(choices=Tournament.Levels.choices)
    description = serializers.CharField(required=False)
    city = serializers.CharField(min_length=3)
    address = serializers.CharField(min_length=3)
    sport = serializers.ChoiceField(choices=Sport.objects.values_list('name', flat=True))
    date = serializers.DateTimeField()
    categories = serializers.ListField(child=serializers.CharField())

    def validate(self, data):
        """Check caegories by sport."""
        category_ids = data.get('categories')
        sport_name = data.get('sport')
        sport = Sport.objects.filter(name=sport_name).last()
        categories = []
        for id in category_ids:
            category = sport.categories.filter(id=id)
            if not category:
                raise serializers.ValidationError(
                    f'The category with id {id} does not exist for this club.')
            categories.append(category)
        self.context['categories'] = categories
        data.pop('categories')
        return data

    def create(self, data):
        """Create tournament and assign the categories."""
        tournament = Tournament.objects.create(**data)
        tournament.categories.add(*self.context['categories'])
        return tournament
