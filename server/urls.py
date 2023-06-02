from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from server.apps.users.urls import urlpatterns as user_urls

api_urls = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include(user_urls)),
]


schema_view = get_schema_view(
    openapi.Info(
        title='Spoty lounge API',
        default_version='v1',
        description='Api spoty lounge app ',
    ),
    public=True,
    patterns=[path('api/v1/', include(api_urls))],
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        'api/v1/swagger/',
        TemplateView.as_view(
            template_name='swagger/swagger.html',
            extra_context={'schema_url': 'openapi-schema'},
        ),
        name='swagger',
    ),
    path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
