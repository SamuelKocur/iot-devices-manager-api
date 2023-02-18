from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from iot.models import Sensor
from iot_devices_manager.utils.permisions import LocalhostOnlyPermission
from iot_devices_manager.utils.serializers import StringListSerializer


class SensorTypesView(GenericAPIView):
    serializer_class = StringListSerializer
    permission_classes = [LocalhostOnlyPermission]

    def get(self, request):
        """Retrieve all sensor types"""
        sensor_types = Sensor.objects.values_list('type', flat=True).distinct()
        serializer = self.serializer_class(sensor_types)
        types = {"sensor_types": serializer.data}
        return Response(types)
