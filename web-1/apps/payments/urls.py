"""Payments URLs."""

from apps.payments.views import PlanViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plans')
urlpatterns = [path('', include(router.urls))]
