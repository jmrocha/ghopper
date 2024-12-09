from ghopper.benchmark_observation import BenchmarkObservation
from ghopper.benchmark_observation_csv_encoder import BenchmarkObservationCSVEncoder
from ghopper.metrics import Metrics
from ghopper.phase_order import PhaseOrder
from unittest import TestCase


class TestBenchmarkObservationCSVEncoder(TestCase):
    def setUp(self):
        metrics = Metrics()
        metrics.cpu_cycles = 10
        metrics.code_size_in_bytes = 100
        self.observation = BenchmarkObservation()
        self.observation.sequence_requested = PhaseOrder("a b")
        self.observation.sequences_executed = [
            PhaseOrder("b a"),
            PhaseOrder("c d"),
        ]
        self.observation.name = "gemm"
        self.observation.has_error = True
        self.observation.error = 'error'
        self.observation.metrics = metrics
        self.encoder = BenchmarkObservationCSVEncoder()
        self.encoder.metrics_encoder = MockMetricsEncoder()

    def test_encode_header(self):
        self.assertEqual(
            self.encoder.encode_header(),
            "name,sequence_requested,sequence_executed,has_error,error"
            ",metric1,metric2"
        )

    def test_encode_body(self):
        body_encoded = self.encoder.encode_body(self.observation)
        self.assertEqual(body_encoded, "gemm,a b,b a;c d,True,\"error\",10,100")


class MockMetricsEncoder:
    def encode_header(self):
        return 'metric1,metric2'

    def encode_body(self, o):
        return '10,100'
