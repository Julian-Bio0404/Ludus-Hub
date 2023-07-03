"""Search URLs."""

from apps.search.views import (ClubDocumentViewSet, TournamentDocumentViewSet,
                               UserDocumentViewSet)
from django.urls import path

urlpatterns = [
    path(
        'search/clubs/',
        ClubDocumentViewSet.as_view({'get': 'list'}),
        name='clubs-search'
    ),

    path(
        'search/tournaments/',
        TournamentDocumentViewSet.as_view({'get': 'list'}),
        name='tournaments-search'
    ),

    path(
        'search/users/',
        UserDocumentViewSet.as_view({'get': 'list'}),
        name='users-search'
    ),
]
