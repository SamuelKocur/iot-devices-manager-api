import requests
import json

from rest_framework import status
from rest_framework.response import Response

from iot_devices_manager.settings import LOOKBACK_URL
from mqtt.topics import BASE_DATA_TOPIC, BASE_SETUP_TOPIC


class MqttAPI:
    lookback_api_url = LOOKBACK_URL + 'api/'
    lookback_mqtt_url = LOOKBACK_URL + 'mqtt/'

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
        url = MqttAPI.lookback_mqtt_url + 'publish/'
        payload = {
            'topic': topic,
            'message': message,
        }

        MqttAPI.send_request(url, payload)

    @staticmethod
    def get_url(topic):
        url = MqttAPI.lookback_api_url
        if str(topic).startswith(BASE_SETUP_TOPIC):
            return url + 'mqtt/save-device/'
        else:
            return url + 'mqtt/save-data/'
