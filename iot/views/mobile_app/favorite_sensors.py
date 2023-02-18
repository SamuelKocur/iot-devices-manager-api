from rest_framework import status
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response

from iot_devices_manager.utils.serializers import EmptySerializer
from user_auth.models import FavoriteSensor
from iot.models import Sensor
from iot.serializers.sensor import SensorDetailSerializer


class FavoriteSensorsListView(GenericAPIView):
    serializer_class = SensorDetailSerializer

    def get(self, request):
        """Retrieve user's favorite sensors"""
        user = request.user
        favorite_sensors = user.favorite_sensors.all()
        sensors = [favorite_sensor.sensor for favorite_sensor in favorite_sensors]
        serializer = self.serializer_class(sensors, many=True, context={'user_id': request.user.id})
        sensors = {"sensors": serializer.data}
        return Response(sensors)


class ToggleFavoriteView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request, sensor_id):
        """
        Save or remove sensor to favorites.
        """
        user_id = request.user.id
        get_object_or_404(Sensor, pk=sensor_id)

        try:
            saved_sensor = FavoriteSensor.objects.get(user_id=user_id, sensor_id=sensor_id)
            saved_sensor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FavoriteSensor.DoesNotExist:
            FavoriteSensor.objects.create(user_id=user_id, sensor_id=sensor_id)
            return Response(status=status.HTTP_201_CREATED)
