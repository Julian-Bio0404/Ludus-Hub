"""Sports models."""

from apps.utils.files import sport_directory_path
from apps.utils.models import BaseAbstractModel, BaseModel
from django.db import models

from .tournaments import Draw, Match, Round


class Sport(BaseModel):
    """Sport model."""

    description = models.TextField(blank=True)

    icon = models.ImageField(
        upload_to=sport_directory_path,
        blank=True,
        null=True
    )

    categories = models.ManyToManyField('sports.Category', blank=True)

    tags = models.ManyToManyField('sports.Tag', blank=True)

    def __str__(self) -> str:
        return self.name


class Rule(BaseAbstractModel):
    """Sport Rules model."""

    sport = models.ForeignKey('sports.Sport', on_delete=models.CASCADE)

    modality = models.ForeignKey('sports.Modality', on_delete=models.CASCADE)

    conditions = models.JSONField(default=dict)

    @classmethod
    def get_default_conditions(self) -> dict:
        """Return default conditions."""
        data = {
            'min-registered': 4,
            'allow-initial-seeds': True,
            'types-draws-allowed': [],
            'type-level-initial-round': '',
            'match-type': ''
        }
        return data

    @classmethod
    def valid_conditions(self) -> bool:
        """Check initial rules conditions."""
        conditions = self.get_default_conditions()
        level_type_round = conditions.get('type-level-initial-round')
        types_draws = conditions.get('types-draws-allowed')
        match_type = conditions.get('match-type')

        valid = level_type_round in [Round.Levels.playoff, Round.Levels.group] \
            and types_draws in Draw.Types.choices and \
            match_type in Match.Types.choices

        return valid

    class Meta:
        unique_together = ('sport', 'modality')
