import json
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from iot.serializers.device import DeviceSerializer


class SaveIoTDataApiView(GenericAPIView):
    """
    Saves data to sensor data model
    """
    permission_classes = [AllowAny]

    def post(self, request):
        body_decoded = str(request.body.decode('utf-8', 'ignore'))
        request_data = json.loads(body_decoded)
        topic = request_data['topic']
        message = request_data['message']

        # Messages.objects.create(
        #     topic=topic,
        #     message=message,
        # ).save()

        # MqttAPI.public_message('slovakia/rabcice/test3/test', 'does it work')  # TODO - publish data to display if needed

        return Response(status=status.HTTP_200_OK)


class SaveIoTDeviceApiView(GenericAPIView):
    """
    Saves devices to Device model
    """
    permission_classes = [AllowAny]
    serializer_class = DeviceSerializer

    def post(self, request, **kwargs):
        """Create a new device"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
