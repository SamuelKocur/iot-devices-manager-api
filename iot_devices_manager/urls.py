from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import iot_devices_manager.view as view

schema_view = get_schema_view(
   openapi.Info(
      title="IoT devices manager API",
      default_version='v1',
      description="Endpoints for IoT device manager.",
      contact=openapi.Contact(email="kocur.samuel253@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny, ),
)

admin.site.site_header = 'IoT devices manager'

urlpatterns = [
    path('', view.index_view, name='index'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('admin/', admin.site.urls),
    path('api/user/', include('user_auth.urls')),
    path('api/mqtt/', include('mqtt.urls')),
    path('api/', include('iot.urls')),
    path('api/data/', include('data_warehouse.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

