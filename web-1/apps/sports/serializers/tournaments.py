"""Tournament serializers."""

from apps.sports.models import Sport, Tournament, Competitor
from apps.sports.serializers import SportModelSerializer, TeamModelSerializer
from apps.users.serializers import UserModelSerializer
from rest_framework import serializers


class TournamentModelSerializer(serializers.ModelSerializer):
    """Tournament model serializer."""

    creator = UserModelSerializer(read_only=True)
    categories = serializers.SerializerMethodField()
    sport = SportModelSerializer(read_only=True)

    def get_categories(self, obj):
        return [c.__str__() for c in obj.categories.all()]

    class Meta:
        """Meta options."""
        model = Tournament
        fields = [
            'id', 'name', 'slug',
            'type', 'level',
            'description', 'city',
            'address', 'sport',
            'date', 'categories',
            'creator', 'referees',
            'created', 'updated'
        ]

    read_only_fields = ['sport', 'categories', 'creator']


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
        category_ids = data.pop('categories')
        sport_name = data.pop('sport')
        sport = Sport.objects.filter(name=sport_name).last()
        categories = []
        for id in category_ids:
            category = sport.categories.filter(id=id).last()
            if not category:
                raise serializers.ValidationError(
                    f'The category with id {id} does not exist for {sport.name}.')
            categories.append(category)
        self.context['categories'] = categories
        self.context['sport'] = sport
        return data

    def create(self, data):
        """Create tournament and assign the categories."""
        tournament = Tournament.objects.create(
            **data,
            sport=self.context['sport'],
            creator=self.context['creator']
        )
        tournament.categories.add(*self.context['categories'])
        return tournament


class AddCompetitorSerializer(serializers.Serializer):
    """
    Add Competitor serializer.
    Util for add a competitor to a tournament.
    """
    pass


class CompetitorModelSerializer(serializers.ModelSerializer):
    """Competitor model serializer."""

    athlete = UserModelSerializer(read_only=True)
    team = TeamModelSerializer(read_only=True)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.__str__()

    class Meta:
        """Meta options."""
        model = Competitor
        fields = [
            'athlete', 'team',
            'category', 'created',
            'updated'
        ]

        read_only_fields = ['athlete', 'team', 'category']
