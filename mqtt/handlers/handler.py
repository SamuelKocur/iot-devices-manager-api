import requests
import json

from rest_framework import status
from rest_framework.response import Response


class MqttAPI:
    base_url = 'http://127.0.0.1:8000/'
    base_api_url = base_url + 'api/'
    base_mqtt_url = base_url + 'mqtt/'

    @staticmethod
    def send_request(url, data):
        response = requests.request("POST", url, data=json.dumps(data))

        if response.status_code == 200:
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handle_message(topic, message):
        url = MqttAPI.base_api_url + 'mqtt/save-data/'
        payload = {
            'topic': topic,
            'message': message,
        }

        MqttAPI.send_request(url, payload)

    @staticmethod
    def public_message(topic, message):
        url = MqttAPI.base_mqtt_url + 'publish/'
        payload = {
            'topic': topic,
            'message': message,
        }

        MqttAPI.send_request(url, payload)

