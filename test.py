# tests the module
import json
import logging as log
import time

import paho.mqtt.client as mqtt

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


def test_simulate():
    """
    prints all the messages present in mqtt
    :return:
    """


if __name__ == "__main__":
    test_simulate_temp_sensors("localhost", 1883)
