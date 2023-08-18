"""Sport adapters."""
from rest_framework import serializers
from sports.models import (Draw, Group, GroupMatch, Match, MatchCompetitor,
                           Round, RoundGroup, RoundMatch, Sport)


class SportAdapter:
    """
    Base Sport Adapter.
    It is a class, util to make the different
    validations that each sport needs to
    create draws and rounds.
    """

    def __init__(self, name) -> None:
        self.name = name

    def get_sport(self):
        try:
            sport = Sport.objects.get(name=self.name)
        except Sport.DoesNotExist:
            sport = None
        return sport

    def get_draw_types(self):
        pass

    def validate(self, data, context):
        pass

    def create_round(self):
        _ = Round.objects.create()

    def create_match(self):
        _ = Match.objects.create()

    def create_match_flow(self):
        _ = MatchCompetitor.objects.create()
        _ = Group.objects.create()
        _ = GroupMatch.objects.create()
        _ = RoundGroup.objects.create()
        _ = RoundMatch.objects.create()

    def create_draw(self):
        _ = Draw.objects.create()
        self.create_round()
        self.create_match()
        self.create_match_flow()


class Karate(SportAdapter):
    """Karate adaptor."""

    def validate(self, data, context):
        type = data.get('type')
        if type not in self.get_draw_types():
            raise serializers.ValidationError(
                f'Type {type} not available for this sport.'
            )
        return data

    def get_draw_types(self):
        types = [
            Draw.Types.single_elimination,
            Draw.Types.double_elimination
        ]
        return types


class Soccer(SportAdapter):
    """Soccer adaptor."""

    pass
