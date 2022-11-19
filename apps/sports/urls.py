"""Sports URLs."""

# Django
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from apps.sports.views import ClubViewSet

router = DefaultRouter()
router.register(r'clubs', ClubViewSet, basename='clubs')
urlpatterns = [path('', include(router.urls))]
