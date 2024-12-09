from ghopper.experiment_observation_csv_encoder import ExperimentObservationCSVEncoder
from ghopper.experiment_observation import ExperimentObservation
from unittest import TestCase

class TestExperimentObservationCSVEncoder(TestCase):
    def setUp(self):
        self.encoder = ExperimentObservationCSVEncoder()
        self.encoder.experiment_metadata_encoder = MockExperimentMetadataEncoder()
        self.encoder.sub_experiment_collection_metadata_encoder = MockSubExperimentCollectionMetadataEncoder()
        self.encoder.sub_experiment_metadata_encoder = MockSubExperimentMetadataEncoder()
        self.encoder.benchmark_observation_encoder = MockBenchmarkObservationEncoder()

    def test_encode_header(self):
        header = self.encoder.encode_header()
        self.assertEqual('1,2,3,4', header)

    def test_encode_body(self):
        body = self.encoder.encode_body(ExperimentObservation())
        self.assertEqual('1,2,3,4', body)

class MockExperimentMetadataEncoder:
    def encode_header(self):
        return '1'
    def encode_body(self, o):
        return '1'

class MockSubExperimentCollectionMetadataEncoder:
    
    def encode_header(self):
        return '2'

    def encode_body(self, o):
        return '2'
class MockSubExperimentMetadataEncoder:
    
    def encode_header(self):
        return '3'

    def encode_body(self, o):
        return '3'
class MockBenchmarkObservationEncoder:
    
    def encode_header(self):
        return '4'

    def encode_body(self, o):
        return '4'
