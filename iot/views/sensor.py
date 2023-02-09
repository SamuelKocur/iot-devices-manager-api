from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404

from iot.models import Device, Sensor, SensorGroup
from iot.serializers.sensor import SensorDetailSerializer


def get_available_sensor_ids(user):
    return SensorGroup.objects.filter(users=user).values_list('available_sensors__id')


class SensorListView(GenericAPIView):
    serializer_class = SensorDetailSerializer

    def get(self, request):
        """Retrieves all available sensors for given user"""
        available_sensors = get_available_sensor_ids(request.user)
        sensors = Sensor.objects.filter(id__in=available_sensors, device__status=Device.Status.APPROVED)
        serializer = self.serializer_class(sensors, many=True, context={'user_id': request.user.id})
        sensors = {"sensors": serializer.data}
        return Response(sensors)


class SensorDetailView(GenericAPIView):
    serializer_class = SensorDetailSerializer

    def get(self, request, sensor_id):
        """Retrieves sensor by id for given user"""
        available_sensors = get_available_sensor_ids(request.user)
        sensor = get_object_or_404(Sensor, pk=sensor_id, id__in=available_sensors, device__status=Device.Status.APPROVED)
        serializer = self.serializer_class(sensor)
        return Response(serializer.data)
