from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404

from iot.models.iot_device import Device, Sensor
from iot.serializers.mobile_app.sensor import SensorDetailSerializer
from iot.utils.permission_checks import get_available_sensor_ids


class SensorListView(GenericAPIView):
    serializer_class = SensorDetailSerializer

    def get(self, request):
        """
        Retrieve all available sensors for given user.
        It is possible to filter those sensors by parameter type.
        """
        available_sensors = get_available_sensor_ids(request.user)
        sensor_type = request.query_params.get("type")
        if sensor_type:
            sensors = Sensor.objects.filter(id__in=available_sensors, device__status=Device.Status.APPROVED, type=sensor_type)
        else:
            sensors = Sensor.objects.filter(id__in=available_sensors, device__status=Device.Status.APPROVED)
        serializer = self.serializer_class(sensors, many=True, context={'user': request.user})
        sensors = {"sensors": serializer.data}
        return Response(sensors)


class SensorDetailView(GenericAPIView):
    serializer_class = SensorDetailSerializer

    def get(self, request, sensor_id):
        """Retrieves sensor by id for given user"""
        available_sensors = get_available_sensor_ids(request.user)
        sensor = get_object_or_404(Sensor, pk=sensor_id, id__in=available_sensors, device__status=Device.Status.APPROVED)
        serializer = self.serializer_class(sensor, context={'user': request.user})
        return Response(serializer.data)
