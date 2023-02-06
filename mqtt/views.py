import json

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from paho.mqtt import publish

import mqtt.constants as constants
from mqtt.cients.data_client import thread as mqtt_thread

mqtt_thread.start()  # starts new thread for MQTT subscribing


class PublishApiView(GenericAPIView):
    """
    Publish data to IoT device which subscribes specific topic
    """
    permission_classes = [AllowAny]

    def post(self, request):
        request_data = json.loads(request.body)
        publish.single(request_data['topic'], request_data['message'], hostname=constants.MQTT_SERVER, port=constants.MQTT_PORT)
        return Response(status=status.HTTP_200_OK)
