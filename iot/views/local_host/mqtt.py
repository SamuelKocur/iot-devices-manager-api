from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
from rest_framework import status

from iot_devices_manager.utils.permissions import LocalhostOnlyPermission
from iot.serializers.device import DeviceDetailSerializer
from iot.serializers.sensor_data import SensorDataRequestSerializer


class SaveIoTDataApiView(GenericAPIView):
    """
    REST API endpoint for saving sensor data
    """
    serializer_class = SensorDataRequestSerializer
    permission_classes = [LocalhostOnlyPermission]

    def post(self, request):
        """Save data to DB for given sensor"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaveIoTDeviceApiView(GenericAPIView):
    """
    REST API endpoint for saving new IoT device
    """
    permission_classes = [LocalhostOnlyPermission]
    serializer_class = DeviceDetailSerializer

    def post(self, request, **kwargs):
        """Create a new device"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
