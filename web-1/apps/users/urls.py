"""Users URLs."""

from apps.users.views import ProfileViewSet, SubscriptionViewSet, UserViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'subscription', SubscriptionViewSet, basename='subscription')
urlpatterns = [path('', include(router.urls))]
