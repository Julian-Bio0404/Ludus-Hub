from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from apps.search.documents import TournamentDocument
from apps.search.serializers import TournamentDocumentSerializer


class TournamentDocumentViewSet(DocumentViewSet):
    """Tournament document viewset."""

    document = TournamentDocument
    serializer_class = TournamentDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FacetedSearchFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
        DefaultOrderingFilterBackend,
        SuggesterFilterBackend,
    ]
    pagination_class = LimitOffsetPagination

    search_fields = (
        'name',
        'type',
        'city',
        'sport.name',
    )

    filter_fields = {
        'id': None,
        'type': 'type',
        'level': 'level',
        'sport': 'sport.name',
    }

    ordering_fields = {
        'id': None,
        'name': 'name',
        'sport': 'sport.name'
    }

    # Default ordering
    ordering = ('id',)

    suggester_fields = {
        'sport_suggest': {
            'field': 'sport.name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'type_suggest': {
            'field': 'type.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'level_suggest': {
            'field': 'level.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        }
    }

    faceted_search_fields = {
        'type': {
            'field': 'type',
            'enabled': True,
        },
        'level': {
            'field': 'level',
            'enabled': True,
        },
        'sport': {
            'field': 'sport.name',
            'enabled': True,
        },
    }
