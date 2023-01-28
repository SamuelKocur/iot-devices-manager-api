from django.urls import path
from iot import views

urlpatterns = [
    path('mqtt/save-data/', views.SaveIoTDataApiView.as_view(), name='save-mqtt-data'),
]
