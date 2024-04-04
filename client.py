import paho.mqtt.client as mqtt
from collections import defaultdict
import json
import logging as log


class UserData:
    def __init__(self, user_id, temp_thresh, thermostat_control):
        self.user_id = user_id
        self.temps = []
        self.heater_state = False
        self.temp_thresh = temp_thresh

        # callback function to turn on the heat
        self.thermostat_control = thermostat_control

    def calculate_heater_state(self):
        data_subset = self.temps[-100:]

        heater_state = True
        for reading in data_subset:
            # if any reading is greater than temp thresh then we don't turn the heater on
            # TODO find a better way of doing this
            if reading > self.temp_thresh:
                heater_state = False

        # turn the heater on
        self.thermostat_control(heater_state, self.user_id)

    def add_temp_reading(self, reading):
        # check the Z-Score and then add/drop the readings.
        # NA for first 100
        if len(self.temps) <= 100:
            self.temps.append(reading)
        else:
            # calculate the Z-Score
            pass


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


        # process the message and take actions if needed
        user_id = message.topic.split("/")[-1]
        message_dict = json.loads(message.payload.decode("utf-8"))


    def on_publish(self, client, userdata, message):
        print("Published the message")
        print(message.topic)


    def switch_heat(self, switch: bool, user_id: str):
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

