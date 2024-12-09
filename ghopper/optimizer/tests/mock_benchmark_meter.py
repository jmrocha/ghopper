from ghopper.metrics import Metrics
from ghopper.benchmark.meter import BenchmarkMeter
from tests.mock_process import MockProcess
from tests.mock_path import MockPath


class MockBenchmarkMeter(BenchmarkMeter):
    def __init__(self):
        super().__init__()
        self._metrics = Metrics()
        self.process = MockProcess()
        self.path = MockPath()
        self.timeout_in_s = -1
        self._error = None

    def return_measure(self, metrics: Metrics):
        self._metrics = metrics

    def measure(self, path: str):
        if self._error:
            raise self._error
        return self._metrics

    def raise_error(self, error):
        self._error = error
