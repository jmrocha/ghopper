from ghopper.benchmark import Benchmark
from ghopper.util.path import Path
from ghopper.benchmark_observation import BenchmarkObservation


class BenchmarkSuite:
    def __init__(self, suite_path: str):
        self.suite_path = suite_path
        self.path = Path()
        self.benchmark_observation: BenchmarkObservation = BenchmarkObservation()
        self.metadata = BenchmarkSuite.Metadata()
        self.benchmark_timeout_in_s = 300
        self.benchmarks = self.get_benchmarks()
        self.subscriber_callback = None

    def get_benchmarks(self):
        files = self.path.glob(self.suite_path, "*.bc")
        benchmarks = []
        for f in files:
            benchmark = Benchmark(f)
            benchmarks.append(benchmark)
        return benchmarks

    def optimize(self, sequence: str) -> None:
        for b in self.benchmarks:
            b.timeout_in_s = self.benchmark_timeout_in_s
            b.subscribe_observation(self.on_benchmark_observed)
            b.optimize(sequence)

    def __getitem__(self, key):
        return self.benchmarks[key]

    def subscribe_observations(self, callback):
        self.subscriber_callback = callback

    def on_benchmark_observed(self, observation: BenchmarkObservation):
        self.observation = observation
        self._push_observation_to_subscriber()

    def _push_observation_to_subscriber(self):
        assert self.observation

        if self.subscriber_callback:
            self.subscriber_callback(self.observation)

    class Metadata:
        def __init__(self):
            self.batch_max_length: int = -1
            self.batch_cardinality: int = -1
            self.suite_name: str = ''


