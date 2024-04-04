# tests the module
import paho.mqtt.client as mqtt

# drop the outliers

def test_simulate_temp_sensors(broker_url, port=1883):
    """
    given a broker url, we simulate 5 temp sensors
    :return:
    """
    # generate test data

    client = mqtt.Client()
    client.connect(broker_url, port=port)

    for i in range(500):
        for j in range(5):
            topic_name = f"temperature_meter/user{j}"
            if i <= 300:
                temp_sample = 30 - (i // 10) - (j // 10)
            else:
                temp_sample = -10 + (i // 10) - (j // 10)
            client.publish(topic_name, temp_sample)


def test_get_all_messages():
    """
    prints all the messages present in mqtt
    :return:
    """
