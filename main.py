from client import MQTTClient
import argparse
import logging as log

def main(broker_url, port, temp_thresh):
    print("Hello")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Sample")
    parser.add_argument("-b", "--broker", help="Broker URL", required=True)
    parser.add_argument("-p", "--port", help="Port of Broker", required=True)
    parser.add_argument("-t", "--temp", help="Temperature threshold", required=True)

    args = parser.parse_args()
    main(args.broker, args.port, args.temp)