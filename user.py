import logging as log

import numpy as np
from scipy.stats import zscore

from utils import STEP_SIZE, OFFSET

log = log.getLogger(__name__)


class UserData:
    def __init__(self, user_id, temp_thresh):
        self.user_id = user_id
        self.temps = []
        self.heater_state = False
        self.temp_thresh = temp_thresh

        log.info(f"Initialized userdata for user {user_id}")

    def add_temp_reading(self, reading, simulate=False):
        log.debug("Adding temperature reading")

        # check the Z-Score and then add/drop the readings.
        # NA for first 100
        if len(self.temps) < OFFSET:
            self.temps.append(reading)
        else:
            self.temps.append(reading)
            if not simulate and self.is_outlier():
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
