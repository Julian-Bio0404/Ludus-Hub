from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    NestedFilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from apps.search.documents import UserDocument
from apps.search.serializers import UserDocumentSerializer


class UserDocumentViewSet(DocumentViewSet):
    """User document viewset."""

    document = UserDocument
    serializer_class = UserDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FacetedSearchFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
        NestedFilteringFilterBackend,
        DefaultOrderingFilterBackend,
        SuggesterFilterBackend,
    ]
    pagination_class = LimitOffsetPagination

    search_fields = (
        'first_name',
        'last_name',
        'username',
    )

    filter_fields = {
        'id': None,
        'role': 'role',
    }

    ordering_fields = {
        'id': None,
        'first_name': 'first_name',
        'last_name': 'last_name',
        'username': 'username',
    }

    # Default ordering
    ordering = ('id',)

    suggester_fields = {
        'first_name_suggest': {
            'field': 'first_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'last_name_suggest': {
            'field': 'last_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'username_suggest': {
            'field': 'username.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        }
    }

    faceted_search_fields = {
        'role': {
            'field': 'role',
            'enabled': True,
        }
    }
