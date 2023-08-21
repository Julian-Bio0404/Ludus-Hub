"""Sport adapters."""

import random
from typing import Union
from datetime import datetime, timedelta

from rest_framework import serializers
from sports.models import (Competitor, Draw, Group, GroupMatch, Match,
                           MatchCompetitor, Round, RoundGroup, Sport)


class SportAdapter:
    """
    Base Sport Adapter.
    It is a class, util to make the different
    validations that each sport needs to
    create draws and rounds.
    """

    def __init__(self, name) -> None:
        self.name = name
        self.sport = self.get_sport()

    def get_sport(self) -> Union[Sport, None]:
        try:
            sport = Sport.objects.get(name=self.name)
        except Sport.DoesNotExist:
            sport = None
        return sport

    def get_draw_types(self) -> list:
        pass

    def get_match_data(self) -> dict:
        data = {
            'title': '',
            'type': Match.Types.individual,
            'state': Match.States.scheduled,
            'date': datetime.now() + timedelta(hours=2)
        }
        return data

    def validate(self, data, context):
        pass

    def create_round(self, draw: Draw, **kwargs) -> Round:
        return Round.objects.create(draw=draw, **kwargs)

    def create_match(self, competitor_count: int) -> list[Match]:
        data = self.get_match_data()
        batch = [Match(**data) for _ in range(competitor_count)]
        return Match.objects.bulk_create(batch)

    def create_match_flow(
        self,
        round: Round,
        competitors: list[Competitor],
        matches: list[Match]
    ) -> None:
        # Create match competitors
        random.shuffle(competitors)
        match_batch = []

        for index, competitor in enumerate(competitors):
            match = random.choice(matches)
            matches.remove(match)
            match_competitor = MatchCompetitor(
                match=match,
                competitor=competitor,
                order=index+1
            )
            match_batch.append(match_competitor)

        match_competitors = MatchCompetitor.objects.bulk_create(match_batch)

        # Create Groups
        group_batch = []
        for i in range(2):
            char = chr(ord('A') + i-1)
            name = f'Group {char}: Round {round.order}'
            group = Group(title=name)
            group_batch.append(group)

        groups = Group.objects.bulk_create(group_batch)

        # Create group matches
        breakpoint = len(match_competitors) // 2
        sub_matches1 = match_competitors[: breakpoint]
        sub_matches2 = match_competitors[breakpoint: len(match_competitors)]
        sub_matches = [sub_matches1, sub_matches2]

        group_matches = []
        for index, sb in enumerate(sub_matches):
            for mc in sb:
                group_match = GroupMatch(
                    group=groups[index],
                    match=mc.match,
                    order=mc.order
                )
                group_matches.append(group_match)

        GroupMatch.objects.bulk_create(group_matches)

        # Create Round Group
        round_group_batch = [RoundGroup(group=group, round=round) for group in groups]
        RoundGroup.objects.bulk_create(round_group_batch)

        # Update Match title
        for match in matches:
            competitor = match.competitors.last()
            match.title = f'Round {round.order}: {competitor.competitor.__str__()}'
        Match.objects.bulk_update(matches, fields=['title'])

        # _ = RoundMatch.objects.create()

    def create_draw(
        self,
        level_type: str,
        competitors: list[Competitor],
        **kwargs
    ) -> Draw:
        self.validate()
        draw = Draw.objects.create(**kwargs)
        kwargs['level_type'] = level_type
        round = self.create_round(draw, **kwargs)
        matches = self.create_match(len(competitors))
        self.create_match_flow(round, competitors, matches)
        return draw


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
