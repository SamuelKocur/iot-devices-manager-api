from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404

from iot.models import Device
from iot.serializers.device import DeviceSerializer


class DeviceListView(GenericAPIView):
    serializer_class = DeviceSerializer

    def get(self, request):
        """Retrieve all devices"""
        device = Device.objects.all()[:20]
        serializer = self.serializer_class(device, many=True, context={'user_id': request.user.id})
        device = {"devices": serializer.data}
        return Response(device)


class DeviceDetailView(GenericAPIView):
    serializer_class = DeviceSerializer

    def get(self, request, device_id):
        """Retrieve device by id"""
        recipe = get_object_or_404(Device, pk=device_id)
        serializer = self.serializer_class(recipe)
        return Response(serializer.data)
