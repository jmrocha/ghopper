from ghopper.benchmark import Benchmark
from ghopper.benchmark.error import *
from ghopper.toolchain.error import *
from ghopper.benchmark_observation import BenchmarkObservation
from ghopper.phase_order import PhaseOrder
from ghopper.metrics import Metrics
from ghopper.benchmark.meter.error import MeterTimeoutError
from tests.toolchain.mock_llvm12 import MockLlvm12
from tests.mock_benchmark_meter import MockBenchmarkMeter
from tests.mock_benchmark import MockBenchmark
from unittest import TestCase, skip


class TestBenchmark(TestCase):
    def setUp(self):
        self.benchmark = Benchmark()
        self.mock_meter = MockBenchmarkMeter()
        self.benchmark.meter = self.mock_meter
        self.benchmark.path = "./gemm.bc"
        self.mock_toolchain = MockLlvm12()
        self.benchmark.toolchain = self.mock_toolchain

    def test_sequence_requested(self):
        self.benchmark.optimize("a b")
        self.assertEqual(PhaseOrder("a b"), self.benchmark.sequence_requested)

    def test_sequences_executed(self):
        self.mock_toolchain.return_optimize([PhaseOrder("b a")])
        self.benchmark.optimize("a b")
        self.assertEqual([PhaseOrder("b a")], self.benchmark.sequences_executed)

    def test_metrics(self):
        metrics = Metrics()
        metrics.cpu_cycles = 10
        self.mock_meter.return_measure(metrics)
        self.benchmark.optimize("a b")
        self.assertEqual(10, self.benchmark.metrics.cpu_cycles)

    def test_observation(self):
        metrics = Metrics()
        metrics.cpu_cycles = 100
        self.mock_meter.return_measure(metrics)
        self.mock_toolchain.return_optimize([PhaseOrder("b a")])
        self.benchmark.optimize("a b")
        self.assertEqual("gemm", self.benchmark.observation.name)
        self.assertEqual(
            PhaseOrder("a b"), self.benchmark.observation.sequence_requested
        )
        self.assertEqual(
            [PhaseOrder("b a")], self.benchmark.observation.sequences_executed
        )
        self.assertEqual(100, self.benchmark.observation.metrics.cpu_cycles)

    def test_push_observation(self):
        mock_callback = MockCallback()
        self.benchmark.subscribe_observation(mock_callback.on_benchmark_observed)
        self.benchmark.optimize("")
        self.assertEqual("gemm", mock_callback.observation.name)

    def test_error(self):
        self.mock_toolchain.raise_error(Llvm12Error('llvm error'))
        try: 
            self.benchmark.optimize('')
        except BenchmarkError:
            self.assertEqual(self.benchmark.has_error, True)
            self.assertEqual(self.benchmark.error, 'gemm: llvm error')

    def test_timeout(self):
        self.mock_meter.raise_error(MeterTimeoutError('timeout'))
        try:
            self.benchmark.optimize('')
        except BenchmarkError:
            self.assertEqual(self.benchmark.has_error, True)
            self.assertEqual(self.benchmark.error, 'gemm: timeout')

class MockCallback:
    def __init__(self):
        self.observation = BenchmarkObservation()

    def on_benchmark_observed(self, obs):
        self.observation = obs

    def test_benchmark_without_main(self):
        self.mock_toolchain.raise_error(ClangError)
        with self.assertRaises(BenchmarkCompileError):
            self.benchmark.optimize("a b")

    def test_benchmark_with_invalid_sequence(self):
        self.mock_toolchain.raise_error(OptError)
        with self.assertRaises(BenchmarkOptimizeError):
            self.benchmark.optimize("a")

    def test_benchmark_timeout(self):
        self.benchmark.timeout_in_s = 5
        self.assertEqual(self.mock_meter.get_timeout_in_s(), 5)

    def test_benchmark_timeout_error(self):
        self.mock_meter.raise_error(MeterTimeoutError)
        with self.assertRaises(BenchmarkTimeoutError):
            self.benchmark.optimize("a")

    def test_benchmark_toolchain_generic_error(self):
        self.mock_toolchain.raise_error(Llvm12Error)
        with self.assertRaises(BenchmarkError):
            self.benchmark.optimize("a")
