"""Sport tasks."""

from __future__ import absolute_import, unicode_literals

from apps.sports.models import Modality, Rule, Sport
from taskapp.celery import app


@app.task(bind=True)
def create_sport_rules(self, id: str, modality_ids: list[str], action: str) -> bool:
    sport = Sport.objects.get(id=id)
    modality_ids = list(set(modality_ids))
    modalities = Modality.objects.filter(id__in=modality_ids)
    if action == 'remove':
        rules = sport.rule_set.filter(modality__in=modalities)
        rules.delete()
    else:
        rules_batch = [
            Rule(
                sport=sport,
                modality=modality,
                conditions=Rule.get_default_conditions()
            ) for modality in modalities
        ]
        Rule.objects.bulk_create(rules_batch, ignore_conflicts=True)
    return True
