from ghopper.experiment_metadata_csv_encoder import ExperimentMetadataCSVEncoder
from ghopper.experiment_metadata import ExperimentMetadata
from unittest import TestCase
import datetime

class TestExperimentMetadataCSVEncoder(TestCase):
    def setUp(self):
        self.encoder = ExperimentMetadataCSVEncoder()

    def test_encode_experiment_metadata_header(self):
        header = self.encoder.encode_header()
        self.assertEqual('experiment_datetime,toolchain,target,dataset_size,benchmark_suite_name', header)

    def test_encode_experiment_metadata_body(self):
        metadata = ExperimentMetadata()
        metadata.experiment_datetime = datetime.datetime(year=2022,month=1,day=1)
        metadata.toolchain = 'toolchain'
        metadata.target = 'target'
        metadata.dataset_size = 'dataset_size'
        metadata.benchmark_suite_name = 'benchmark_suite_name'
        body = self.encoder.encode_body(metadata)
        self.assertEqual('2022-01-01 00:00:00,toolchain,target,dataset_size,benchmark_suite_name', body)
