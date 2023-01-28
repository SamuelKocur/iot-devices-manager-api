import json

import paho.mqtt.client as mqtt

import mqtt.constants as constants
from .handler import MqttAPI
from .topics import BASE_TOPIC


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(BASE_TOPIC+'#')
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, message):
    decoded_message = str(message.payload.decode("utf-8", "ignore"))
    json_message = json.loads(decoded_message)

    print(f'Received message on topic: {message.topic} with payload: {message.payload}')
    MqttAPI.handle_message(message.topic, json_message)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(constants.MQTT_USER, constants.MQTT_PASSWORD)
client.connect(
    host=constants.MQTT_SERVER,
    port=constants.MQTT_PORT,
    keepalive=constants.MQTT_KEEPALIVE
)
