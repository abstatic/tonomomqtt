import paho.mqtt.client as mqtt
from collections import defaultdict


class MQTTClient:
    """
    MQTT client which turns the heat on based on temperature sensor readings

    stores state (offset), heating settings, temperature records last 500 readings ono a per user basis in a dict
    """

    data_state = defaultdict()

    def __init__(self, broker_url):
        """
        create a mqtt client and do a ".loop_start()"
        """
        pass

    def on_connect(self):
        """
        on connection, we subscribe to topics
        :return:
        """
        pass

    def on_message(self):
        """
        on getting a message do this
        :return:
        """

    def
