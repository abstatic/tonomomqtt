from client import MQTTClient
import sys
import argparse

def main():
    print("Hello")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--broker", help="Broker URL")
    parser.add_argument("-p", "--port", help="Port of Broker")
    parser.add_argument("-t", "--temp", help="Temperature threshold")

    args = parser.parse_args()
    main()