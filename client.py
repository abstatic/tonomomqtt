import paho.mqtt.client as mqtt
from collections import defaultdict
import json
import logging as log


class MQTTClient:
    """
    MQTT client which turns the heat on based on temperature sensor readings
    subscribes to all temperature readings
    publishes to heating system of a user

    stores state (offset), heating settings, temperature records last 500 readings ono a per user basis in a dict
    """

    data_state = defaultdict()

    def __init__(self, broker_url, port, temp_thresh):
        """
        create a mqtt client and do a ".loop_start()"
        """
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        # self.client.on_disconnect
        # self.client.on_subscribe

        self.temp_thresh = temp_thresh

        try:
            self.client.connect(broker_url, port)
        except Exception as e:
            log.error(f"Failed to create mqtt client {e}")

    def on_connect(self, client, obj, flags, rc):
        """
        on connection, we subscribe to topics
        :return:
        """
        log.info("Connected to broker. Subscribing to topics")
        self.client.subscribe("temperature_meter/#", qos=2)

    def on_message(self, client, userdata, message):
        """
        on getting a message do this
        :return:
        """
        print(f"I received a message {message}")
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        print("message qos=", message.qos)
        print("message retain flag=", message.retain)

    def on_publish(self, client, userdata, message):
        print("Published the message")
        print(message.topic)

    def switch_heat(self, switch: bool, user_id: int):
        """
        :param switch: state for the thermostat, False-> off True -> On
        :param user_id: user_id for which to take action
        :return: Nothing.
        """
        if not switch:
            action = "turn_off"
        else:
            action = "turn_on"
        payload = {
            "action": action
        }
        self.client.publish(f"heating_system/{user_id}/control", json.dumps(payload), qos=2, retain=True)

