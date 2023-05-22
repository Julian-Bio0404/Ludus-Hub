"""Tournament serializers."""

from apps.sports.models import Competitor, Sport, Team, Tournament
from apps.sports.serializers import SportModelSerializer, TeamModelSerializer
from apps.users.models import User
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
    athlete = serializers.CharField(required=False)
    team = serializers.CharField(required=False)
    category_id = serializers.UUIDField(required=False)

    def validate(self, data):
        """Check the competitor and category."""
        athlete_name = data.get('athlete')
        team_name = data.get('team')
        category_id = data.get('category_id')
        tournament = self.context['tournament']

        if not athlete_name and not team_name:
            raise serializers.ValidationError('Add an athlete or a team')
        if athlete_name and team_name:
            raise serializers.ValidationError('Add an athlete or a team, not both')

        if athlete_name:
            competitor = tournament.competitor_set.filter(
                athlete__username=athlete_name,
                category__id=category_id
            )
            try:
                self.context['athlete'] = User.objects.get(username=athlete_name)
            except User.DoesNotExist:
                raise serializers.ValidationError('The user does not exist')
        elif team_name:
            competitor = tournament.competitor_set.filter(
                team__slug=team_name,
                category__id=category_id
            )
            try:
                self.context['team'] = Team.objects.get(slug=team_name)
            except Team.DoesNotExist:
                raise serializers.ValidationError('The team does not exist')

        category = tournament.categories.filter(id=category_id).last()
        if not category:
            raise serializers.ValidationError('The category does not exist')
        self.context['category'] = category

        if competitor.exists():
            raise serializers.ValidationError(
                'The competitor already is registered for this category')

        return data

    def create(self, data):
        return Competitor.objects.create(**self.context)


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
