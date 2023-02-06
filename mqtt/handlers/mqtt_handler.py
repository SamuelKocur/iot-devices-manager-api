import requests
import json

from rest_framework import status
from rest_framework.response import Response

from mqtt.topics import BASE_DATA_TOPIC, BASE_SETUP_TOPIC


class MqttAPI:
    base_url = 'http://127.0.0.1:8000/'
    base_api_url = base_url + 'api/'
    base_mqtt_url = base_url + 'mqtt/'

    @staticmethod
    def send_request(url, data):
        headers = {'Content-type': 'application/json'}
        response = requests.request("POST", url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handle_message(topic, message):
        url = MqttAPI.get_url(topic)
        MqttAPI.send_request(url, message)

    @staticmethod
    def public_message(topic, message):
        url = MqttAPI.base_mqtt_url + 'publish/'
        payload = {
            'topic': topic,
            'message': message,
        }

        MqttAPI.send_request(url, payload)

    @staticmethod
    def get_url(topic):
        url = MqttAPI.base_api_url
        if str(topic).startswith(BASE_SETUP_TOPIC):
            return url + 'mqtt/save-device/'
        else:
            return url + 'mqtt/save-data/'
