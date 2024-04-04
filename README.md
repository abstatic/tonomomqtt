* uses paho-mqtt library for MQTT
* Logic for calculating when to turn on/off the heater should be more optimized.

- Use TS db for
    - Function to pre process heater state on each insertion
    - maintain mean , std deviation , variance of readings
    - Historical data storage
    - influx / timescale DB


- Useful Commands
    - `mosquitto_pub -t temperature_meter/{} -f ./data`
    - `python main.py`
    - `mosquitto_sub -t temperature_meter/#`