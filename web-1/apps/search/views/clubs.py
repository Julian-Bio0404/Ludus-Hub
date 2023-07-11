"""Club elasticsearch views."""

from apps.search.documents import ClubDocument
from apps.search.serializers import ClubDocumentSerializer
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend, FacetedSearchFilterBackend,
    FilteringFilterBackend, OrderingFilterBackend, SearchFilterBackend,
    SuggesterFilterBackend)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet


class ClubDocumentViewSet(DocumentViewSet):
    """User document viewset."""

    document = ClubDocument
    serializer_class = ClubDocumentSerializer
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

    search_fields = {
        'name': {'boost': 3},
        'slug': {'boost': 4},
        'city': {'boost': 2}
    }

    filter_fields = {
        'id': None,
        'sport': 'sport.name'
    }

    ordering_fields = {
        'id': None,
        'name': 'name'
    }

    # Default ordering
    ordering = ('_score', 'id',)

    suggester_fields = {
        'name_suggest': {
            'field': 'name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }

    faceted_search_fields = {
        'sport': {
            'field': 'sport.name',
            'enabled': True,
        }
    }
