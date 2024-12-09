from .error import *
from ghopper.phase_order import PhaseOrder
from ghopper.benchmark_observation import BenchmarkObservation
from ghopper.metrics import Metrics
from ghopper.benchmark.meter import BenchmarkMeter, MeterError
from ghopper.toolchain.llvm12 import *
from pathlib import Path

BENCHMARK_BIN_PATH = "/tmp/benchmark"


class Benchmark:
    def __init__(self, path: str = ""):
        self.timeout_in_s = 300
        self.path: str = path
        self.meter: BenchmarkMeter = BenchmarkMeter()
        self.toolchain = Llvm12()
        self.sequence_requested: PhaseOrder = PhaseOrder()
        self.sequences_executed: PhaseOrder = [PhaseOrder()]
        self.subscriber_callback = None
        self.metrics = Metrics()
        self.observation = BenchmarkObservation()
        self.has_error = False
        self.error = ''

    def optimize(self, sequence_str: str = "") -> None:
        assert self.path, "benchmark path needs to be defined"

        self.sequence_requested = self._get_sequence_from_str(sequence_str)
        self._try_optimize()
        self.observation = self._get_observation()
        self._push_observation_to_subscriber()

    def _try_optimize(self):
        try:
            self.sequences_executed = self._try_emit_optimized_binary()
            self.metrics = self._try_measurement()
        except Exception as e:
            self.has_error = True
            self.error = f'{self._get_name()}: {e}'

    def _push_observation_to_subscriber(self):
        if self.subscriber_callback:
            self.subscriber_callback(self.observation)

    def _get_sequence_from_str(self, sequence_str: str) -> PhaseOrder:
        return PhaseOrder(sequence_str)

    def _try_emit_optimized_binary(self) -> list[PhaseOrder]:
        assert self.toolchain
        assert self.path
        assert self.sequence_requested
        return self.toolchain.optimize(self.path, self.sequence_requested.sequence)

    def _try_measurement(self) -> Metrics:
        self.meter.timeout_in_s = self.timeout_in_s
        return self.meter.measure(BENCHMARK_BIN_PATH)

    def _get_observation(self) -> BenchmarkObservation:
        observation = BenchmarkObservation()
        observation.name = self._get_name()
        observation.sequence_requested = self.sequence_requested
        observation.sequences_executed = self.sequences_executed
        observation.metrics = self.metrics
        observation.has_error = self.has_error
        observation.error = self.error
        return observation

    def _get_name(self) -> str:
        assert type(self.path) is str

        return Path(self.path).stem

    def __eq__(self, o) -> bool:
        return self.path == o.path

    def subscribe_observation(self, callback):
        self.subscriber_callback = callback
