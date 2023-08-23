"""Sports URLs."""

from apps.sports.views import (AssistanceViewSet, ClubViewSet,
                               CompetitorViewSet, DrawViewSet,
                               InvitationViewSet, MemberViewSet, SportViewSet,
                               TeamViewset, TournamentViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'clubs', ClubViewSet, basename='clubs')

router.register(
    r'clubs/(?P<slug>[a-zA-Z0-9_-]+)/members', MemberViewSet, basename='members')

router.register(
    r'clubs/(?P<slug>[a-zA-Z0-9_-]+)/invitations', InvitationViewSet, basename='invitations')

router.register(
    r'clubs/(?P<slug>[a-zA-Z0-9_-]+)/assistances', AssistanceViewSet, basename='assistances')

router.register(
    r'clubs/(?P<slug>[a-zA-Z0-9_-]+)/teams', TeamViewset, basename='teams')

router.register(r'sports', SportViewSet, basename='sports')

router.register(r'tournaments', TournamentViewSet, basename='tournaments')

router.register(
    r'tournaments/(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/competitors',
    CompetitorViewSet,
    basename='competitors'
)

router.register(
    r'tournaments/(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/draws',
    DrawViewSet,
    basename='draws'
)

urlpatterns = [path('', include(router.urls))]
