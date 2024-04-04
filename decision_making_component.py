import argparse
import logging

from client import MQTTClient
from utils import OFFSET, STEP_SIZE


def main(broker_url, port, temp_thresh):
    logging.basicConfig(
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        level=logging.INFO,
    )
    logging.info(
        f"Starting client with offset: {OFFSET} and step size: {STEP_SIZE} temp thres {temp_thresh}"
    )
    client = MQTTClient(broker_url, port, temp_thresh)
    client.mqtt_client.loop_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Sample")
    parser.add_argument("-b", "--broker", help="Broker URL", required=True, type=str)
    parser.add_argument("-p", "--port", help="Port of Broker", required=True, type=int)
    parser.add_argument(
        "-t", "--temp", help="Temperature threshold", required=True, type=float
    )

    args = parser.parse_args()
    main(args.broker, args.port, args.temp)
