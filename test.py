# tests the module
import json
import logging as log
import time
import unittest

import paho.mqtt.client as mqtt

from client import MQTTClient
from user import UserData

log.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    level=log.INFO,
)


# drop the outliers
def test_simulate_temp_sensors(broker_url, port=1883):
    """
    given a broker url, we simulate 5 temp sensors
    :return:
    """
    # generate test data
    k = 0
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.connect(broker_url, port=port)
    log.info("Connected to broker, sending data")
    for i in range(10):
        for j in range(2):
            topic_name = f"temperature_meter/user{j}"
            if i <= 300:
                temp_sample = 20 - (i // 10) - (j // 10)
            else:
                temp_sample = -10 + (i // 10) - (j // 10)
            log.info(f"{k} publishing to {topic_name} {temp_sample}")
            k += 1
            payload = {"temperature": float(temp_sample)}
            client.publish(topic_name, json.dumps(payload))
            time.sleep(1)


class TestHeatingSystem(unittest.TestCase):

    def setUp(self):
        # Initialize MQTTClient with mock broker URL, port, and a test threshold
        self.mqtt_client = MQTTClient("localhost", 1883, 15)

        # Add a test user
        self.user_id = "user1"
        self.mqtt_client.data_state[self.user_id] = UserData(
            self.user_id, self.mqtt_client.temp_thresh
        )

    def test_heating_turned_on_when_cold(self):
        # Simulate receiving cold temperature readings below the threshold
        for temp in [10] * 300:
            self.mqtt_client.data_state[self.user_id].add_temp_reading(temp)

        self.assertTrue(
            self.mqtt_client.data_state[self.user_id].heater_state,
            "Heater should be turned on for cold temperatures",
        )

    def test_outlier_detection(self):
        for temp in [20] * 300:
            self.mqtt_client.data_state[self.user_id].add_temp_reading(temp)
        before_len = len(self.mqtt_client.data_state[self.user_id].temps)

        for temp in [100] * 300:
            self.mqtt_client.data_state[self.user_id].add_temp_reading(temp)
        after_len = len(self.mqtt_client.data_state[self.user_id].temps)

        self.assertEqual(before_len, after_len)

    def test_heating_turned_off_when_warm(self):
        # First, simulate the heater being turned on by cold temperatures
        for temp in [10] * 300:  # Cold temperatures
            self.mqtt_client.data_state[self.user_id].add_temp_reading(temp, True)

        # Then, simulate receiving warm temperature readings above the threshold
        for temp in [20] * 300:  # Warm temperatures
            self.mqtt_client.data_state[self.user_id].add_temp_reading(temp, True)

        self.assertFalse(
            self.mqtt_client.data_state[self.user_id].heater_state,
            "Heater should be turned off for warm temperatures",
        )


if __name__ == "__main__":
    unittest.main()
    # test_simulate_temp_sensors("localhost", 1883)
