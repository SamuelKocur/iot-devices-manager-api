from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404

from iot.models import Device
from iot.serializers.device import DeviceDetailSerializer
from iot_devices_manager.utils.permissions import LocalhostOnlyPermission


class DeviceListView(GenericAPIView):
    serializer_class = DeviceDetailSerializer
    permission_classes = [LocalhostOnlyPermission]

    def get(self, request):
        """Retrieve all devices"""
        devices = Device.objects.all()[:20]
        serializer = self.serializer_class(devices, many=True)
        devices = {"devices": serializer.data}
        return Response(devices)


class DeviceDetailView(GenericAPIView):
    serializer_class = DeviceDetailSerializer
    permission_classes = [LocalhostOnlyPermission]

    def get(self, request, device_id):
        """Retrieve device by id"""
        device = get_object_or_404(Device, pk=device_id)
        serializer = self.serializer_class(device)
        return Response(serializer.data)
