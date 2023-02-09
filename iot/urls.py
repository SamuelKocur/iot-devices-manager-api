from django.urls import path
from iot.views import mqtt, device, sensor, location

urlpatterns = [
    path('devices/', device.DeviceListView().as_view(), name="recent_devices"),
    path('devices/<str:device_id>/', device.DeviceDetailView().as_view(), name="single_device"),
    path('sensors/', sensor.SensorListView().as_view(), name="recent_sensors"),
    path('sensors/<int:sensor_id>/', sensor.SensorDetailView().as_view(), name="single_sensor"),
    path('locations/', location.LocationListView().as_view(), name="all_locations"),

    path('mqtt/save-data/', mqtt.SaveIoTDataApiView.as_view(), name='save-mqtt-data'),
    path('mqtt/save-device/', mqtt.SaveIoTDeviceApiView.as_view(), name='save-mqtt-device'),
]
