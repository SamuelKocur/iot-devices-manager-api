from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="IoT devices manager API",
      default_version='v1',
      description="Endpoints for IoT device manager.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="kocur.samuel253@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny, ),
)

admin.site.site_header = 'IoT devices manager'

urlpatterns = [
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('admin/', admin.site.urls),
    path('api/auth/', include('user_auth.urls')),
    path('mqtt/', include('mqtt.urls')),
    path('api/', include('iot.urls')),
]
