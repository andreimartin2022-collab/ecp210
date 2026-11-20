"""this'll be the connection to the ecp210 through matlab.

SimulatedBackend stands in until we make the matlab communication,
so this is just a little visualizer with the same methods,
power_on, power_off, set_input, stop, read.
"""
import threading
import time


class SimulatedBackend:
    """three masses in a chain driven by the motor input.
    Masses, springs, and damping are placeholders obviously. not real ECP values."""

    def __init__(self):
        self.m = [1.0, 1.0, 1.0]
        self.k_wall = 400.0       # spring from mass 1 to the wall
        self.k = [400.0, 400.0]   # springs between masses 1-2 and 2-3
        self.c = 2.0              # damping on each mass
        self.x = [0.0, 0.0, 0.0]  # positions
        self.v = [0.0, 0.0, 0.0]  # velocities
        self.u = 0.0              # input voltage
        self.powered = False
        self._lock = threading.Lock()
        self._last = time.time()

    def _step(self):
        now = time.time()
        dt = min(now - self._last, 2.0)
        self._last = now
        n = max(1, int(dt / 0.001))
        h = dt / n
        x, v = self.x, self.v
        for _ in range(n):
            f1 = self.u - self.k_wall * x[0] - self.k[0] * (x[0] - x[1]) - self.c * v[0]
            f2 = self.k[0] * (x[0] - x[1]) - self.k[1] * (x[1] - x[2]) - self.c * v[1]
            f3 = self.k[1] * (x[1] - x[2]) - self.c * v[2]
            for i, f in enumerate((f1, f2, f3)):
                v[i] += f / self.m[i] * h
                x[i] += v[i] * h

    def power_on(self):
        with self._lock:
            self._step()
            self.powered = True

    def power_off(self):
        with self._lock:
            self._step()
            self.u = 0.0
            self.powered = False

    def set_input(self, volts):
        with self._lock:
            self._step()
            self.u = volts

    def stop(self):
        with self._lock:
            self._step()
            self.u = 0.0

    def read(self):
        with self._lock:
            self._step()
            return {"positions": list(self.x), "input": self.u, "powered": self.powered}