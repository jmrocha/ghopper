from ghopper.benchmark_suite import BenchmarkSuite
from ghopper.benchmark_observation import BenchmarkObservation
from tests.mock_benchmark import MockBenchmark


class MockBenchmarkSuite(BenchmarkSuite):
    def __init__(self, path = 'mock'):
        super().__init__(path)
        self.benchmarks = [MockBenchmark("a.bc"), MockBenchmark("b.bc")]
        self._log = []

    def get_log(self):
        return " ".join(self._log)

    def subscribe_observations(self, callback):
        self._log += ["subscribe"]
        super().subscribe_observations(callback)

    def optimize(self, sequence):
        self._log += ["optimize"]
        super().optimize(sequence)
