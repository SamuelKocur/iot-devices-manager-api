from django.urls import path
from iot.views import mqtt, device

urlpatterns = [
    path('devices/', device.DeviceListView().as_view(), name="recent_devices"),
    path('devices/<int:device_id>/', device.DeviceDetailView().as_view(), name="single_device"),

    path('mqtt/save-data/', mqtt.SaveIoTDataApiView.as_view(), name='save-mqtt-data'),
    path('mqtt/save-device/', mqtt.SaveIoTDeviceApiView.as_view(), name='save-mqtt-device'),
]
