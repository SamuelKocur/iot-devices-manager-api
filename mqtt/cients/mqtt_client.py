import json
import threading

import paho.mqtt.client as mqtt

import mqtt.constants as constants
from mqtt.handlers.mqtt_handler import MqttAPI
from mqtt.topics import BASE_DATA_TOPIC, BASE_SETUP_TOPIC


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f'Connected successfully to MQTT Broker - subscribing {BASE_DATA_TOPIC}, {BASE_SETUP_TOPIC}')
        client.subscribe(BASE_DATA_TOPIC + '#')
        client.subscribe(BASE_SETUP_TOPIC + '#')
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, message):
    decoded_message = str(message.payload.decode("utf-8", "ignore"))
    json_message = json.loads(decoded_message)
    print(f'Received message on topic: {message.topic} with payload: {message.payload}')
    MqttAPI.handle_message(message.topic, json_message)


def mqtt_loop():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.username_pw_set(constants.MQTT_USER, constants.MQTT_PASSWORD)
    mqtt_client.connect(
        host=constants.MQTT_SERVER,
        port=constants.MQTT_PORT,
        keepalive=constants.MQTT_KEEPALIVE
    )
    mqtt_client.loop_forever()


thread = threading.Thread(target=mqtt_loop)
