"""Tournament models."""

from apps.utils.models import SportfyModel, SportModel
from django.db import models
from djchoices import ChoiceItem, DjangoChoices
from mptt.models import MPTTModel, TreeForeignKey


class Tournament(SportModel):
    """Tournament model."""

    class Types(DjangoChoices):
        """Tournament types."""
        open = ChoiceItem('open', 'Open')
        qualifying = ChoiceItem('qualifying', 'Qualifying')
        ranking = ChoiceItem('ranking', 'Ranking')
        shampionship = ChoiceItem('shampionship', 'Shampionship')

    class Levels(DjangoChoices):
        """Tournament levels."""
        local = ChoiceItem('local', 'Local')
        departmental = ChoiceItem('departmental', 'Departmental')
        national = ChoiceItem('national', 'National')
        international = ChoiceItem('international', 'International')

    type = models.CharField(choices=Types.choices, max_length=12)

    level = models.CharField(choices=Levels.choices, max_length=13)

    description = models.TextField(blank=True)

    city = models.CharField(max_length=60, blank=True)

    address = models.CharField(max_length=60, blank=True)

    sport = models.ForeignKey(
        'sports.Sport',
        on_delete=models.PROTECT
    )

    date = models.DateTimeField()

    categories = models.ManyToManyField('sports.Category', blank=True)

    referees = models.ManyToManyField('users.User', blank=True)

    def __str__(self) -> str:
        return self.name


class Competitor(SportfyModel):
    """
    Competitor model.
    can store the athlete or a team
    """

    athlete = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    team = models.ForeignKey(
        'sports.Team',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    category = models.ForeignKey(
        'sports.Category',
        on_delete=models.PROTECT
    )

    tournament = models.ForeignKey(
        'sports.Tournament',
        on_delete=models.SET_DEFAULT,
        default=0
    )

    def __str__(self) -> str:
        """Return athlete """
        if self.athlete:
            return self.athlete.get_full_name()
        return self.team.name


class Rating(SportfyModel):
    """Rating model."""

    competitor = models.ForeignKey('sports.Competitor', on_delete=models.CASCADE)

    score = models.FloatField()

    def __str__(self) -> str:
        return self.score


class Draw(SportfyModel):
    """Draw model."""

    class Types(DjangoChoices):
        """Round types."""
        all_play_all = ChoiceItem('all_play_all', 'All Play All')

        single_elimination = ChoiceItem('single_elimination', 'Single Elimination')

        single_elimination_playoff = ChoiceItem(
            'single_elimination_playoff', 'Single Elimination Playoff')

        double_elimination = ChoiceItem('double_elimination', 'Double Elimination')

    type = models.CharField(choices=Types.choices, max_length=26)

    category = models.ForeignKey(
        'sports.Category',
        on_delete=models.PROTECT
    )

    tournament = models.ForeignKey(
        'sports.Tournament',
        on_delete=models.SET_DEFAULT,
        default=0
    )

    def __str__(self) -> str:
        return f'Draw from {self.tournament.name}'


class Round(SportfyModel, MPTTModel):
    """Round model."""

    class Types(DjangoChoices):
        """Round types."""
        all_play_all = ChoiceItem('all_play_all', 'All Play All')

        single_elimination = ChoiceItem('single_elimination', 'Single Elimination')

        single_elimination_playoff = ChoiceItem(
            'single_elimination_playoff', 'Single Elimination Playoff')

        double_elimination = ChoiceItem('double_elimination', 'Double Elimination')

    class Levels(DjangoChoices):
        """Level types."""
        group = ChoiceItem('group', 'Group')
        playoff = ChoiceItem('playoff', 'Playoff')
        semifinal = ChoiceItem('semifinal', 'Semifinal')
        bronze = ChoiceItem('bronze', 'Bronze')
        final = ChoiceItem('final', 'Final')

    type = models.CharField(choices=Types.choices, max_length=26)

    level_type = models.CharField(
        choices=Levels.choices,
        max_length=9,
        default=Levels.playoff
    )

    tournament = models.ForeignKey(
        'sports.Tournament',
        on_delete=models.SET_DEFAULT,
        default=0
    )

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    draw = models.ForeignKey('sports.Draw', on_delete=models.CASCADE)

    matches = models.ManyToManyField(
        'sports.Match',
        through='sports.RoundMatch',
        through_fields=('round', 'match')
    )

    order = models.SmallIntegerField(default=1)

    def __str__(self) -> str:
        return f'Round {self.order}: {self.type}'


class RoundMatch(SportfyModel):
    """
    Round Match model.
    Acts as an intermediate model between Round and Match.
    """

    round = models.ForeignKey('sports.Round', on_delete=models.CASCADE)

    match = models.ForeignKey('sports.Match', on_delete=models.CASCADE)

    order = models.SmallIntegerField(default=1)

    def __str__(self) -> str:
        """Return username and club."""
        return f'Match #{self.order} from {self.round}'


class Match(SportfyModel):
    """Match model."""

    class Types(DjangoChoices):
        """Match types."""
        group = ChoiceItem('group', 'Group')
        versus = ChoiceItem('versus', 'Versus')

    class States(DjangoChoices):
        """Match states."""
        scheduled = ChoiceItem('scheduled', 'Scheduled')
        playing = ChoiceItem('playing', 'Playing')
        paused = ChoiceItem('paused', 'Paused')

    type = models.CharField(choices=Types.choices, max_length=6)

    state = models.CharField(choices=States.choices, max_length=9)

    competitors = models.ManyToManyField(
        'sports.Competitor',
        through='sports.MatchCompetitor',
        through_fields=('match', 'competitor')
    )

    def __str__(self) -> str:
        return self.type


class MatchCompetitor(SportfyModel):
    """Match Competitor."""

    match = models.ForeignKey('sports.Match', on_delete=models.CASCADE)

    competitor = models.ForeignKey('sports.Competitor', on_delete=models.CASCADE)

    rating = models.ForeignKey(
        'sports.Rating',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    order = models.SmallIntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.competitor} from {self.match}'
