import logging as log

import numpy as np
from scipy.stats import zscore

from utils import STEP_SIZE, OFFSET

log = log.getLogger(__name__)


class UserData:
    def __init__(self, user_id, temp_thresh, thermostat_control):
        self.user_id = user_id
        self.temps = []
        self.heater_state = False
        self.temp_thresh = temp_thresh

        # callback function to turn on the heat
        self.thermostat_control = thermostat_control

        log.info(f"Initialized userdata for user {user_id}")

    def calculate_heater_state(self):
        """
        takes window of last 100 temperature readings
        ONLY IF all the temp readings are below THRESHOLD -> Turn on the heater
        ONLY IF all the temp readings are above THRESHOLD -> Turn off the heater
        """
        log.info("Calculating heater state")
        data_subset = self.temps[-STEP_SIZE:]

        # default is on, if there is temp reading of higher then we turn it off
        heater_state = "on"
        for reading in data_subset:
            # if any reading is greater than temp thresh then we don't turn the heater on
            # TODO find a better way of doing this maybe take average?
            if reading > self.temp_thresh:
                heater_state = "off"
        # if still on, then turn the heater on
        if heater_state == "on":
            # turn the heater on
            log.info(f"Turning on heater for {self.user_id}")
            self.heater_state = heater_state
            self.thermostat_control(heater_state, self.user_id)
        else:
            # also check if temp has continuously been more than thresh then we turn off heating
            # we start with 'off'
            heater_state = "off"
            for reading in data_subset:
                if reading < self.temp_thresh:
                    heater_state = "on"
            if heater_state == "off":
                log.info(f"Turning off the heater for {self.user_id}")
                self.heater_state = heater_state
                self.thermostat_control(heater_state, self.user_id)

    def add_temp_reading(self, reading):
        log.debug("Adding temperature reading")

        # check the Z-Score and then add/drop the readings.
        # NA for first 100
        if len(self.temps) < OFFSET:
            self.temps.append(reading)
        else:
            self.temps.append(reading)
            if self.is_outlier():
                log.info(f"Outlier detected {reading}")
                self.temps.pop()
                return False, None

            if (
                np.mean(self.temps[-STEP_SIZE:]) < self.temp_thresh
                and not self.heater_state
            ):
                log.info("Turning the heater on")
                self.heater_state = True
                return True, "turn_on"
            elif (
                np.mean(self.temps[-STEP_SIZE:]) >= self.temp_thresh
                and self.heater_state
            ):
                self.heater_state = False
                return True, "turn_off"

        return False, None

    def is_outlier(self):
        # Apply Z-score for outlier detection
        if len(self.temps) < 2:
            return False
        zs = zscore(self.temps)
        return abs(zs[-1]) > 3
