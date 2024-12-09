from ghopper.benchmark_suite_observation_csv_encoder import (
        BenchmarkSuiteObservationCSVEncoder)
from ghopper.benchmark_suite_observation import BenchmarkSuiteObservation
from unittest import TestCase

class MockBenchmarkObservationCSVEncoder:
    def encode_header(self):
        return 'mock_benchmark_obs'

    def encode_body(self, o):
        return 'mock_benchmark_obs'

class TestBenchmarkSuiteObservationCSVEncoder(TestCase):
    def setUp(self):
        self.mock_benchmark_encoder = MockBenchmarkObservationCSVEncoder()
        self.encoder = BenchmarkSuiteObservationCSVEncoder()
        self.encoder.benchmark_observation_encoder = self.mock_benchmark_encoder

    def test_encode_header(self):
        header = self.encoder.encode_header() 
        self.assertEqual(header, 
                'benchmark_suite,batch_max_length,batch_cardinality,mock_benchmark_obs')

    def test_encode_body(self):
        obs = BenchmarkSuiteObservation()
        obs.suite_name = 'suite X'
        obs.batch_max_length = 12
        obs.batch_cardinality = 10
        encoded = self.encoder.encode_body(obs)
        self.assertEqual(encoded, 'suite X,12,10,mock_benchmark_obs')
