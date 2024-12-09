from ghopper.sub_experiment_collection_metadata_csv_encoder import SubExperimentCollectionMetadataCSVEncoder
from ghopper.sub_experiment_collection_metadata import SubExperimentCollectionMetadata
from unittest import TestCase

class TestSubExperimentCollectionMetadataCSVEncoder(TestCase):
    def setUp(self):
        self.encoder = SubExperimentCollectionMetadataCSVEncoder()

    def test_encode_header(self):
        encoded = self.encoder.encode_header()
        self.assertEqual('requested_phase_order_lengths,requested_phase_order_cardinalities,strategy,strategy_seed', encoded)

    def test_encode_body(self):
        metadata = SubExperimentCollectionMetadata()
        metadata.requested_phase_order_lengths = '10,20'
        metadata.requested_phase_order_cardinalities = '2,22'
        metadata.strategy = 'strategy'
        metadata.strategy_seed = 'strategy_seed'
        encoded = self.encoder.encode_body(metadata)
        self.assertEqual('"10,20","2,22",strategy,strategy_seed', encoded)

    def test_encode_null_seed(self):
        metadata = SubExperimentCollectionMetadata()
        metadata.requested_phase_order_lengths = '10,20'
        metadata.requested_phase_order_cardinalities = '2,22'
        metadata.strategy = 'strategy'
        metadata.strategy_seed = None 
        encoded = self.encoder.encode_body(metadata)
        self.assertEqual('"10,20","2,22",strategy,N/A', encoded)

