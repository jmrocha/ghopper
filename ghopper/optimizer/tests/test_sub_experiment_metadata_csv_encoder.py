from ghopper.sub_experiment_metadata_csv_encoder import SubExperimentMetadataCSVEncoder
from ghopper.sub_experiment_metadata import SubExperimentMetadata
from unittest import TestCase
class TestSubExperimentMetadataCSVEncoder(TestCase):
    def setUp(self):
        self.encoder = SubExperimentMetadataCSVEncoder()

    def test_encode_header(self):
        header = self.encoder.encode_header()
        self.assertEqual('phase_order_max_length,phase_order_cardinality', header)

    def test_encode_body(self):
        metadata = SubExperimentMetadata()
        metadata.phase_order_max_length = 10
        metadata.phase_order_cardinality = 20
        body = self.encoder.encode_body(metadata)
        self.assertEqual('10,20', body)
