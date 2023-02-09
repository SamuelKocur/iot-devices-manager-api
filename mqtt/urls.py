from django.urls import path
from mqtt.publisher import views

urlpatterns = [
    path('publish/', views.PublishApiView.as_view(), name='publish'),
]
