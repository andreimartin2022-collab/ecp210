import math
import threading


class KitError(Exception):
    """A command that isn't allowed in the kit's current state."""


class Kit:
    def __init__(self, backend, v_max):
        self.backend = backend
        self.v_max = v_max
        self.state = "OFF"
        self._lock = threading.Lock()

    def power_on(self):
        with self._lock:
            if self.state == "OFF":
                self.backend.power_on()
                self.state = "IDLE"

    def power_off(self):
        with self._lock:
            self.backend.power_off()
            self.state = "OFF"

    def set_input(self, volts):
        with self._lock:
            if self.state == "OFF":
                raise KitError("The kit is off")
            if self.state == "FAULT":
                raise KitError("Clear the fault before sending inputs")
            if not math.isfinite(volts) or abs(volts) > self.v_max:
                raise KitError(f"Input must be between -{self.v_max} and {self.v_max} V")
            self.backend.set_input(volts)
            self.state = "RUNNING" if volts != 0 else "IDLE"

    def emergency_stop(self):
        with self._lock:
            self.backend.stop()
            if self.state != "OFF":
                self.state = "FAULT"

    def reset(self):
        with self._lock:
            if self.state == "FAULT":
                self.backend.stop()
                self.state = "IDLE"

    def status(self):
        with self._lock:
            return {"state": self.state, **self.backend.read()}