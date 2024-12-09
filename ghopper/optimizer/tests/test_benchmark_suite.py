from ghopper.benchmark_suite import BenchmarkSuite
from ghopper.benchmark_suite_observation import BenchmarkSuiteObservation
from ghopper.benchmark import Benchmark
from ghopper.benchmark_observation import BenchmarkObservation
from tests.mock_path import MockPath
from tests.mock_benchmark import MockBenchmark
from tests.mock_benchmark_suite import BenchmarkSuite
from unittest import TestCase, skip


class TestBenchmarkSuite(TestCase):
    def setUp(self):
        self.path_mock = MockPath()
        self.path_mock.return_glob(["./suite/a.bc", "./suite/b.bc"])
        self.suite = BenchmarkSuite("./suite/")
        self.suite.name = 'suite X'
        self.suite.path = self.path_mock
        self.suite.benchmarks = [MockBenchmark("a.bc"), MockBenchmark("b.bc")]

    def test_get_benchmarks(self):
        bench_list = self.suite.get_benchmarks()
        self.assertEqual(
            bench_list, [Benchmark("./suite/a.bc"), Benchmark("./suite/b.bc")]
        )

    def test_optimize(self):
        self.suite.optimize("x y")
        self.assertEqual(self.suite[0].log, "subscribe a.bc: <x y>")
        self.assertEqual(self.suite[1].log, "subscribe b.bc: <x y>")
