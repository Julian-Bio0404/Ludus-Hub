"""Tournament models."""

from apps.utils.models import BaseAbstractModel, BaseModel
from django.db import models
from djchoices import ChoiceItem, DjangoChoices
from mptt.models import MPTTModel, TreeForeignKey


class Tournament(BaseModel):
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

    creator = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

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

    referees = models.ManyToManyField(
        'users.User',
        related_name='tournaments_as_referee',
        blank=True
    )

    def __str__(self) -> str:
        return self.name


class Competitor(BaseAbstractModel):
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
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self) -> str:
        """Return athlete """
        if self.athlete:
            return self.athlete.get_full_name()
        return self.team.name


class Rating(BaseAbstractModel):
    """Rating model."""

    competitor = models.ForeignKey('sports.Competitor', on_delete=models.CASCADE)

    score = models.FloatField()

    def __str__(self) -> str:
        return self.score


class Draw(BaseAbstractModel):
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
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'Draw from {self.tournament.name}'


class Round(BaseAbstractModel, MPTTModel):
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
        default=Levels.playoff,
        verbose_name='level'
    )

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    draw = models.ForeignKey('sports.Draw', on_delete=models.CASCADE)

    groups = models.ManyToManyField(
        'sports.Group',
        through='sports.RoundGroup',
        through_fields=('round', 'group')
    )

    matches = models.ManyToManyField(
        'sports.Match',
        through='sports.RoundMatch',
        through_fields=('round', 'match')
    )

    order = models.SmallIntegerField(default=1)

    def __str__(self) -> str:
        return f'Round {self.order}: {self.type}'


class RoundGroup(BaseAbstractModel):
    """
    Round Group model.
    Acts as an intermediate model between Round and Group.
    """

    round = models.ForeignKey('sports.Round', on_delete=models.CASCADE)

    group = models.ForeignKey('sports.Group', on_delete=models.CASCADE)

    order = models.SmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Matches Group'

    def __str__(self) -> str:
        """Return username and club."""
        return f'Group #{self.order}'


class Group(BaseAbstractModel):
    """
    Group model.
    It is a Group of matches.
    """

    title = models.CharField(max_length=300, null=True)

    matches = models.ManyToManyField(
        'sports.Match',
        through='sports.GroupMatch',
        through_fields=('group', 'match')
    )

    class Meta:
        verbose_name_plural = 'Matches Groups'

    def __str__(self) -> str:
        return self.title


class RoundMatch(BaseAbstractModel):
    """
    Round Match model.
    Acts as an intermediate model between Round and Match.
    """

    round = models.ForeignKey('sports.Round', on_delete=models.CASCADE)

    match = models.ForeignKey('sports.Match', on_delete=models.CASCADE)

    order = models.SmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Match'

    def __str__(self) -> str:
        """Return username and club."""
        return f'Match #{self.order} from {self.round}'


class GroupMatch(BaseAbstractModel):
    """
    Group Match model.
    Acts as an intermediate model between Group and Match.
    """

    group = models.ForeignKey('sports.Group', on_delete=models.CASCADE)

    match = models.ForeignKey('sports.Match', on_delete=models.CASCADE)

    order = models.SmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Match Group'

    def __str__(self) -> str:
        """Return username and club."""
        return f'Match #{self.order}'


class Match(BaseAbstractModel):
    """Match model."""

    class Types(DjangoChoices):
        """Match types."""
        individual = ChoiceItem('individual', 'Individual')
        versus = ChoiceItem('versus', 'Versus')
        group = ChoiceItem('group', 'Group')

    class States(DjangoChoices):
        """Match states."""
        scheduled = ChoiceItem('scheduled', 'Scheduled')
        playing = ChoiceItem('playing', 'Playing')
        paused = ChoiceItem('paused', 'Paused')

    title = models.CharField(max_length=300, null=True)

    type = models.CharField(choices=Types.choices, max_length=10)

    state = models.CharField(choices=States.choices, max_length=9)

    competitors = models.ManyToManyField(
        'sports.Competitor',
        through='sports.MatchCompetitor',
        through_fields=('match', 'competitor')
    )

    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Matches'

    def __str__(self) -> str:
        return self.title


class MatchCompetitor(BaseAbstractModel):
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
        return f'{self.competitor.__str__()}'
