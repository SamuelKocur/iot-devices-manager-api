import json
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import Messages


class SaveIoTDataApiView(GenericAPIView):
    """
    Sass user by username and password
    """
    permission_classes = [AllowAny]

    def post(self, request):
        body_decoded = str(request.body.decode('utf-8', 'ignore'))
        request_data = json.loads(body_decoded)
        topic = request_data['topic']
        message = request_data['message']

        Messages.objects.create(
            topic=topic,
            message=message,
        ).save()

        # MqttAPI.public_message('slovakia/rabcice/test3/test', 'does it work')  # TODO - publish data to display if needed

        return Response(status=status.HTTP_200_OK)
