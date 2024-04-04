* uses paho-mqtt library for MQTT


* python main.py -h

* Logic for calculating when to turn on/off the heater should be more optimized.

- Use TS db for
    - Function to pre process heater state on each insertion
    - maintain mean , std deviation , variance of readings
    - Historical data storage
    - `docker pull influxdb:2.7.5`
    -


- Useful Commands
    - `mosquitto_pub -t temperature_meter/{} -f ./data`
    - `python main.py`
    - `mosquitto_sub -t temperature_meter/#`
    - 
