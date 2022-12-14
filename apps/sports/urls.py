"""Sports URLs."""

# Django
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from apps.sports.views import ClubViewSet, MemberViewSet, InvitationViewSet

router = DefaultRouter()
router.register(r'clubs', ClubViewSet, basename='clubs')
router.register(
    r'clubs/(?P<slug>[a-zA-Z0-9_-]+)/members', MemberViewSet, basename='members')

router.register(
    r'clubs/(?P<slug>[a-zA-Z0-9_-]+)/invitations', InvitationViewSet, basename='invitations')

urlpatterns = [path('', include(router.urls))]
