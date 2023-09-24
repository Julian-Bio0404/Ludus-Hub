"""Tournament serializers."""

from apps.sports.adapters import SPORT_ADAPTERS_MAPPING
from apps.sports.models import (Category, Competitor, Draw, RefereeInvitation,
                                Round, Rule, Sport, Team, Tournament)
from apps.sports.serializers import (CategoryModelSerializer,
                                     SportModelSerializer, TeamModelSerializer)
from apps.users.models import User
from apps.users.serializers import UserModelSerializer
from django.db.models import Q
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
    sport = serializers.CharField(min_length=3)
    date = serializers.DateTimeField()
    categories = serializers.ListField(child=serializers.CharField())

    def validate(self, data):
        """Check caegories by sport."""
        category_ids = data.pop('categories')
        sport_name = data.pop('sport')
        sport = Sport.objects.filter(name=sport_name).last()
        if not sport:
            raise serializers.ValidationError(
                f'The sport with name {sport_name} does not available')
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


class RoundModelSerializer(serializers.ModelSerializer):
    """Round model serializer."""

    class Meta:
        """Meta options."""
        model = Round
        fields = [
            'id', 'type',
            'level_type', 'order',
            'groups', 'matches',
            'created', 'updated'
        ]


class CreateDrawSerializer(serializers.Serializer):
    """
    Create draw serializer.
    Handle the creation of tournament draws.
    """

    category_id = serializers.UUIDField()
    type = serializers.ChoiceField(choices=Draw.Types.choices)
    initial_seeds = serializers.ListField(child=serializers.CharField(), required=False)

    def validate(self, data):
        category_id = data.get('category_id')
        initial_seeds = data.get('initial_seeds')
        tournament = self.context['tournament']

        try:
            category = tournament.categories.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError('The category does not exist')

        self.context['category'] = category

        rule = Rule.objects.get(
            sport=tournament.sport,
            modality=category.modality
        )

        if not rule.valid_conditions():
            raise serializers.ValidationError(
                f'The rules of {category.modality.name} are not yet available')

        self.context['conditions'] = rule.conditions

        competitor_seeds = []
        if initial_seeds:
            for seed in initial_seeds:
                competitor = tournament.competitor_set.filter(
                    Q(athlete__username=seed) | Q(team__slug=seed),
                    category__id=category_id
                ).last()
                if not competitor:
                    raise serializers.ValidationError(
                        f'The competitor {seed} does not exist for this category')
                competitor_seeds.append(competitor)

        if competitor_seeds:
            self.context['competitor_seeds'] = competitor_seeds

        return data

    def create(self, data):
        """Create draw and rounds."""
        tournament = self.context['tournament']
        category = self.context['category']
        conditions = self.context['conditions']
        competitors = list(tournament.competitor_set.all())
        sport_name = tournament.sport.name.lower()
        adapter = SPORT_ADAPTERS_MAPPING[sport_name]

        draw = adapter.create_draw(
            level_type=conditions.get('type-level-initial-round'),
            competitors=competitors,
            type=data['type'],
            category=category,
            tournament=tournament
        )

        return draw


class DrawModelSerializer(serializers.ModelSerializer):
    """Draw model serializer."""

    category = CategoryModelSerializer(read_only=True)
    rounds = serializers.SerializerMethodField(read_only=True)

    def get_rounds(self, obj):
        rounds = obj.round_set.all()
        return RoundModelSerializer(rounds, many=True).data

    class Meta:
        """Meta options."""
        model = Draw
        fields = [
            'id', 'type',
            'category', 'rounds',
            'created', 'updated'
        ]
        read_only_fields = ['category', 'rounds']


class AddAdminSerializer(serializers.Serializer):
    """Add a admin to a tournament"""

    usernames = serializers.ListField(child=serializers.CharField())
    action = serializers.ChoiceField(choices=['add', 'remove'])

    def validate(self, data):
        usernames = data['usernames']
        users = User.objects.filter(username__in=usernames)
        self.context['users'] = users
        return data

    def save(self, **kwargs):
        action = self.data['action']
        tournament = self.context['tournament']
        if action == 'add':
            tournament.administrators.add(*self.context['users'])
        elif action == 'remove':
            tournament.administrators.remove(*self.context['users'])
        return tournament


class RefereeInvitationModelSerializer(serializers.ModelSerializer):
    """Referee invitation model serializer."""

    sent_by = UserModelSerializer(read_only=True)
    invited = UserModelSerializer(read_only=True)

    class Meta:
        """Meta options."""
        model = RefereeInvitation
        fields = [
            'id', 'sent_by', 'invited',
            'used', 'created', 'updated'
        ]


class CreateRefereeInvitationSerializer(serializers.Serializer):
    """Create referee invitation serializer."""

    usernames = serializers.ListField(child=serializers.CharField())

    def validate(self, data):
        usernames = data['usernames']
        tournament = self.context['tournament']
        referee_ids = tournament.referees.values_list('id', flat=True)
        invited_ids = tournament.referee_invitations.values_list('invited__id', flat=True)
        user_ids = list(referee_ids) + list(invited_ids)
        users = User.objects.filter(username__in=usernames).exclude(id__in=user_ids)
        self.context['users'] = users
        return data

    def save(self, **kwargs):
        tournament = self.context['tournament']
        users = self.context['users']
        batch = [
            RefereeInvitation(
                sent_by=self.context['creator'],
                invited=user,
                tournament=tournament
            ) for user in users
        ]
        invitations = RefereeInvitation.objects.bulk_create(batch)
        tournament.referee_invitations.add(*invitations)
        return invitations
