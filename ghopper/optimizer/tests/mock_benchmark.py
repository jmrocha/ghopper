from ghopper.benchmark import Benchmark
from ghopper.benchmark.error import BenchmarkError
from tests.toolchain.mock_llvm12 import MockLlvm12
from tests.mock_path import MockPath
from tests.mock_benchmark_meter import MockBenchmarkMeter


class MockBenchmark(Benchmark):
    def __init__(self, path: str = ""):
        super().__init__(path)
        self.log = ""
        self.meter = MockBenchmarkMeter()
        self.toolchain = MockLlvm12()

    def optimize(self, sequence):
        self.log += f"{self.path}: <{sequence}>"
        super().optimize(sequence)

    def subscribe_observation(self, callback):
        self.log += "subscribe "
        super().subscribe_observation(callback)
