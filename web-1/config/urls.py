"""URL Configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.users.urls', 'users'), namespace='users')),
    path('', include(('apps.sports.urls', 'sports'), namespace='sports')),
    path('', include(('apps.payments.urls', 'payments'), namespace='plans')),
    path('', include(('apps.search.urls', 'search'), namespace='search'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
