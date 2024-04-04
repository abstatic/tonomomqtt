import json
import logging as log
import traceback
from typing import Dict

import paho.mqtt.client as mqtt

from user import UserData

log = log.getLogger(__name__)


class MQTTClient:
    """
    MQTT client which turns the heat on based on temperature sensor readings
    subscribes to all temperature readings
    publishes to heating system of a user

    stores state (offset), heating settings, temperature records last 500 readings ono a per user basis in a dict
    """

    data_state: Dict[str, UserData] = {}

    def __init__(self, broker_url, port, temp_thresh):
        """
        create a mqtt client and do a ".loop_start()"
        """
        self.offset = 0
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_subscribe = self.on_subscribe
        self.mqtt_client.on_publish = self.on_publish

        # self.client.on_disconnect
        # self.client.on_subscribe

        self.temp_thresh = temp_thresh

        try:
            self.mqtt_client.connect(broker_url, port)
        except Exception as e:
            log.error(f"Failed to create mqtt client {e}")
            traceback.print_exc()

    def on_connect(self, client, obj, flags, rc):
        """
        on connection, we subscribe to topics
        :return:
        """
        log.info("Connected to broker. Subscribing to topics")
        self.mqtt_client.subscribe("temperature_meter/#", qos=2)

    def on_subscribe(self, client, userdata, mid, reason_code_list):
        log.info("Subbed")

    def on_message(self, client, userdata, message):
        """
        on getting a message do this
        :return:
        """
        log.debug(
            f"message received topic: {message.topic} for {str(message.payload.decode('utf-8'))}"
        )

        try:
            # process the message and take actions if needed
            if str(message.topic).startswith("temperature_meter"):
                user_id = message.topic.split("/")[-1]
                message_dict = json.loads(message.payload.decode("utf-8"))
                temp_reading = float(message_dict["temperature"])

                if user_id not in self.data_state:
                    self.data_state[user_id] = UserData(user_id, self.temp_thresh, self.switch_heat)
                user = self.data_state[user_id]

                action_required, action = user.add_temp_reading(temp_reading)
                if action_required:
                    control_topic = f"heating_system/{user_id}/control"
                    self.mqtt_client.publish(control_topic, json.dumps({"action": action}))
                    log.info(f"Published '{action}' to {control_topic}")
                # user.add_temp_reading(temp_reading)
        except Exception as e:
            log.error(f"Failed in processing message {e}")
            traceback.print_exc()

    def on_publish(self, client, userdata, message):
        log.info(f"Published")

    def switch_heat(self, switch: str, user_id: str):
        """
        :param switch: state for the thermostat, False-> off True -> On
        :param user_id: user_id for which to take action
        :return: Nothing.
        """
        if switch == "off":
            action = "turn_off"
        else:
            action = "turn_on"

        payload = {"action": action}
        log.info(
            f"Publishing to heating_system/{user_id}/control , payload: {json.dumps(payload)}"
        )
        self.mqtt_client.publish(
            f"heating_system/{user_id}/control", json.dumps(payload), qos=2, retain=True
        )
