#### Local Setup

- Setup a virtualenv using `virtualenv .venv` (in the directory of your choice)
- `pip install -r requirements.txt` to install required dependencies
- Start using `python decision_making_component.py -b localhost -p 1883 -t 20`
- Testing `python test.py`
- For mosquitto publishing `mosquitto_pub -t temperature_meter/{} -f ./data`
- Follow allong using `mosquitto_sub -t temperature_meter/#`

#### How it works

* uses paho-mqtt library for MQTT
* `OFFSET` : After How many steps we start doing outlier detection
* `STEP_SIZE` : Lookback window size for calculating mean. Running
* OFFSET and STEPSIZE is defined in utils file, defaults to 100
* `client.py` contains implementation of MQTT client
* `user.py` contains implementation of UserData class, for tracking state at user level.
* `test.py` for test files

#### Testing

* `test_simulate_temp_sensors` method is for quick simulation, with 1sec sleep
* Unittest cases for checking heater state for user
* Testing requires a live broker. Broker is not mocked
* Test cases are affected by value of OFFSET and STEP_SIZE

#### Could be better

    - tests for outlier detection
    - Mocking of broker
    - Use TS db like influx / timescale - maintain running mean, std deviation, variance
    - Historical data storage
    - Crash handling