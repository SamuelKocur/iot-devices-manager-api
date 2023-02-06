import json

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import rest_framework.serializers as serializers

from paho.mqtt import publish

import mqtt.constants as constants
from mqtt.cients.mqtt_client import thread as mqtt_thread

mqtt_thread.start()  # starts new thread for MQTT subscribing


class PublishApiSerializer(serializers.Serializer):
    topic = serializers.CharField()
    message = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class PublishApiView(GenericAPIView):
    """
    Publish data to IoT device which subscribes specific topic
    """
    permission_classes = [AllowAny]
    serializer_class = PublishApiSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            publish.single(serializer.data['topic'], serializer.data['message'], hostname=constants.MQTT_SERVER, port=constants.MQTT_PORT)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
