import time


class Timer:
    def __init__(self):
        self.time: time = time
        self._start_timestamp: float = -1
        self._stop_timestamp: float = -1

    def start(self):
        self._start_timestamp = self.time.perf_counter_ns()

    def stop(self):
        self._stop_timestamp = self.time.perf_counter_ns()

    def time_elapsed_in_ns(self):
        return self._stop_timestamp - self._start_timestamp
