from time import time


class Scheduler:

    def __init__(self, simulation_speed: float, down_sampling: int):
        self.simulation_speed = simulation_speed
        self.down_sampling = down_sampling

        self._running = False
        self._index = 0
        self._now = time()
        self._timestamp = self._now

        self._time_array = None
        self._data_array = None
        self._length = 0
        self._period = 0.002

    def __getitem__(self, index):
        return None if self._data_array is None else self._data_array[index]

    def __iter__(self):
        yield from [] if self._data_array is None else self._data_array

    @property
    def value(self):
        return self[self._index, :]

    def start(self, time_array=None, data_array=None):
        if time_array is not None and data_array is not None:
            self._time_array = time_array
            self._data_array = data_array
            self._length = len(time_array)
            self._period = 0.002 # CALCULATE THIS FROM DATA
            self._timestamp = time()
        self._running = True

    def stop(self):
        self._running = False

    def reset(self):
        self._index = 0

    def step_forward(self) -> bool:
        if self._index < self._length:
            self._index += 1
            return True
        else:
            return False

    def step_backward(self) -> bool:
        if self._index > 0:
            self._index -= 1
            return True
        else:
            return False

    def update(self):
        self._now = time()
        result = False

        time_passed = self._now - self._timestamp
        self._index = int(time_passed / self._period)
        if self._index >= self._length:
            self._index = self._length - 1
            self.stop()

        return False