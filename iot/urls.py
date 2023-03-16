from django.urls import path
from iot.views.local_host import mqtt, sensor_type, device
from iot.views.mobile_app import favorite_sensors, location, sensor, user_customization

urlpatterns = [
    path('devices/', device.DeviceListView().as_view(), name="recent_devices"),
    path('devices/<str:device_id>/', device.DeviceDetailView().as_view(), name="single_device"),

    path('sensors/', sensor.SensorListView().as_view(), name="recent_sensors"),
    path('sensors/<int:sensor_id>/', sensor.SensorDetailView().as_view(), name="single_sensor"),
    path('sensors/favorites/', favorite_sensors.FavoriteSensorsListView().as_view(), name="favorites_sensors"),
    path('sensors/<int:sensor_id>/toggle-favorite/', favorite_sensors.ToggleFavoriteView().as_view(), name="toggle_favorite"),
    path('sensors/types/', sensor_type.SensorTypesView().as_view(), name="sensor_types"),
    path('sensors/<int:sensor_id>/user-customization', user_customization.UserSensorNameView.as_view(), name="customize_user_sensor_name"),

    path('locations/', location.LocationListView().as_view(), name="all_locations"),
    path('locations/<int:location_id>/', location.LocationDetailView().as_view(), name="single_location"),
    path('locations/<int:location_id>/user-customization', user_customization.UserLocationNameView.as_view(), name="customize_user_location_name"),

    path('mqtt/save-data/', mqtt.SaveIoTDataApiView.as_view(), name='save-mqtt-data'),
    path('mqtt/save-device/', mqtt.SaveIoTDeviceApiView.as_view(), name='save-mqtt-device'),
]
