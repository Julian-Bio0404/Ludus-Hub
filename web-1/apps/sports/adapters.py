"""Sport adapters."""

import random
from datetime import datetime, timedelta
from typing import Union

from apps.sports.models import (Competitor, Draw, Group, GroupMatch, Match,
                                MatchCompetitor, Round, RoundGroup, RoundMatch,
                                Sport)
from rest_framework import serializers


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
        self.draw = None

    def get_sport(self) -> Union[Sport, None]:
        try:
            sport = Sport.objects.get(name__iexact=self.name)
        except Sport.DoesNotExist:
            sport = None
        return sport

    def get_draw_types(self) -> list:
        return list(Draw.Types.labels.keys())

    def get_match_data(self) -> dict:
        data = {
            'title': '',
            'type': Match.Types.individual,
            'state': Match.States.scheduled,
            'date': datetime.now() + timedelta(hours=2)
        }
        return data

    def validate(self, data: dict, context: dict) -> dict:
        type = data.get('type')
        if type not in self.get_draw_types():
            raise serializers.ValidationError(
                f'Type {type} not available for this sport.'
            )
        return data

    def create_round(self, draw: Draw, **kwargs) -> Round:
        return Round.objects.create(draw=draw, **kwargs)

    def create_match(self, competitor_count: int) -> list[Match]:
        data = self.get_match_data()
        batch = [Match(**data) for _ in range(competitor_count)]
        return Match.objects.bulk_create(batch)

    def add_competitors_to_match(
        self,
        competitors: list[Competitor],
        matches: list[Match]
    ) -> list[MatchCompetitor]:
        match_type = matches[0].type
        random.shuffle(competitors)
        match_batch = []

        if match_type == Match.Types.individual:
            for index, competitor in enumerate(competitors):
                match = random.choice(matches)
                matches.remove(match)
                match_competitor = MatchCompetitor(
                    match=match,
                    competitor=competitor,
                    order=index+1
                )
                match_batch.append(match_competitor)

        elif match_type == Match.Types.versus:
            while competitors:
                match = random.choice(matches)
                matches.remove(match)
                competitors_sample = random.sample(competitors, 2)
                for cs in competitors_sample:
                    competitors.remove(cs)
                    match_competitor = MatchCompetitor(
                        match=match,
                        competitor=cs,
                        order=index+1
                    )
                    match_batch.append(match_competitor)

        return MatchCompetitor.objects.bulk_create(match_batch)

    def create_groups(self, round: Round, count: int) -> list[Group]:
        group_batch = [
            Group(
                title=f"Group {chr(ord('A') + i-1)}: Round {round.order}"
            ) for i in range(count)
        ]
        return Group.objects.bulk_create(group_batch)

    def get_submatches(self, matches: list[Match], count: int) -> list[list[Match]]:
        sublist_length = len(matches) // count
        submatches = []
        for i in range(0, len(submatches), sublist_length):
            submatch = submatches[i:i + sublist_length]
            submatches.append(submatch)
        return submatches

    def create_match_flow(
        self,
        round: Round,
        competitors: list[Competitor],
        matches: list[Match]
    ) -> None:
        # Create match competitors
        self.add_competitors_to_match(competitors, matches)

        # Create Groups
        count = 2
        groups = self.create_groups(round, count)

        # Create group matches
        submatches = self.get_submatches(matches, count)

        group_matches = []
        for index, submatch in enumerate(submatches):
            for match in submatch:
                group_match = GroupMatch(
                    group=groups[index],
                    match=match,
                    order=index+1
                )
                group_matches.append(group_match)

        GroupMatch.objects.bulk_create(group_matches)

        # Create Round Group
        round_group_batch = [RoundGroup(group=group, round=round) for group in groups]
        RoundGroup.objects.bulk_create(round_group_batch)

    def get_match_title(self, match: Match, round: Round) -> str:
        competitor1 = match.competitors.first().competitor
        if match.type == Match.Types.individual:
            title = f'Round {round.order}: {competitor1.__str__()}'
        elif match.type == Match.Types.versus:
            competitor2 = match.competitors.last().competitor
            title = f'Round {round.order}: {competitor1.__str__()} vs {competitor2.__str__()}'
        return title

    def update_matches(self, matches: list[Match], round: Round) -> None:
        """Update Match title."""
        for match in matches:
            match.title = self.get_match_title(match, round)
        Match.objects.bulk_update(matches, fields=['title'])

    def create_draw(
        self,
        level_type: str,
        competitors: list[Competitor],
        **kwargs
    ) -> Draw:
        self.validate()
        self.draw = Draw.objects.create(**kwargs)
        kwargs['level_type'] = level_type
        round = self.create_round(self.draw, **kwargs)
        matches = self.create_match(len(competitors))
        self.create_match_flow(round, competitors, matches)
        self.update_matches(matches, round)
        return self.draw


class KarateAdapter(SportAdapter):
    """Karate adaptor."""

    def __init__(self) -> None:
        super().__init__('karate')

    def get_draw_types(self):
        types = [
            Draw.Types.single_elimination,
            Draw.Types.double_elimination
        ]
        return types

    def get_match_data(self) -> dict:
        data = super().get_match_data()
        if self.draw.type == Draw.Types.single_elimination:
            type = Match.Types.individual
        else:
            type = Match.Types.versus
        data['type'] = type
        return data

    def create_match_flow(
        self,
        round: Round,
        competitors: list[Competitor],
        matches: list[Match]
    ) -> None:
        if self.draw.type == Draw.Types.single_elimination:
            return super().create_match_flow(round, competitors, matches)
        elif self.draw.type == Draw.Types.double_elimination:
            self.add_competitors_to_match(competitors, matches)
            batch = []
            for index, match in matches:
                round_match = RoundMatch(round=round, match=match, order=index+1)
                batch.append(round_match)
            RoundMatch.objects.bulk_create(batch)


class SoccerAdapter(SportAdapter):
    """Soccer adaptor."""

    def __init__(self) -> None:
        super().__init__('soccer')

    def get_draw_types(self) -> list:
        types = [
            Draw.Types.all_play_all,
            Draw.Types.group_stage_and_playoffs
        ]
        return types

    def get_match_data(self) -> dict:
        data = super().get_match_data()
        data['type'] = Match.Types.versus
        return data

    def create_groups(self, round: Round, count: int) -> list[Group]:
        group_batch = [
            Group(title=f"Group {chr(ord('A') + i-1)}") for i in range(count)
        ]
        return Group.objects.bulk_create(group_batch)

    def create_match_flow(
        self,
        round: Round,
        competitors: list[Competitor],
        matches: list[Match]
    ) -> None:
        # Create match competitors
        self.add_competitors_to_match(competitors, matches)

        if self.draw.type == Draw.Types.all_play_all:
            batch = []
            for index, match in matches:
                round_match = RoundMatch(round=round, match=match, order=index+1)
                batch.append(round_match)
            RoundMatch.objects.bulk_create(batch)

        elif self.draw.type == Draw.Types.group_stage_and_playoffs:
            # Create Groups
            count = len(competitors) // 4
            groups = self.create_groups(round, count)

            # Create group matches
            submatches = self.get_submatches(matches, count)

            group_matches = []
            for index, submatch in enumerate(submatches):
                for match in submatch:
                    group_match = GroupMatch(
                        group=groups[index],
                        match=match,
                        order=index+1
                    )
                    group_matches.append(group_match)

            GroupMatch.objects.bulk_create(group_matches)

            # Create Round Group
            round_group_batch = [RoundGroup(group=group, round=round) for group in groups]
            RoundGroup.objects.bulk_create(round_group_batch)

    def get_match_title(self, match: Match, round: Round) -> str:
        competitor1 = match.competitors.first().competitor
        competitor2 = match.competitors.last().competitor
        title = f'{competitor1.__str__()} vs {competitor2.__str__()}'
        return title


SPORT_ADAPTERS_MAPPING = {
    'karate': KarateAdapter,
    'soccer': SoccerAdapter
}
