import json

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mqtt.cients.mqtt import client as mqtt_client


class PublishApiView(GenericAPIView):
    """
    Publish data to IoT device which subscribes specific topic
    """
    permission_classes = [AllowAny]

    def post(self, request):
        request_data = json.loads(request.body)
        rc, mid = mqtt_client.publish(request_data['topic'], request_data['message'])
        return Response(
            rc,
            status=status.HTTP_200_OK,
        )
