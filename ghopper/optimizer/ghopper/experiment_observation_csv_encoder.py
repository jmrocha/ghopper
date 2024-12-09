from ghopper.benchmark_suite_observation_csv_encoder import BenchmarkSuiteObservationCSVEncoder
from ghopper.experiment_metadata_csv_encoder import ExperimentMetadataCSVEncoder
from ghopper.sub_experiment_collection_metadata_csv_encoder import SubExperimentCollectionMetadataCSVEncoder
from ghopper.sub_experiment_metadata_csv_encoder import SubExperimentMetadataCSVEncoder
from ghopper.benchmark_observation_csv_encoder import BenchmarkObservationCSVEncoder

class ExperimentObservationCSVEncoder:
    def __init__(self):
        self.experiment_metadata_encoder = ExperimentMetadataCSVEncoder()
        self.sub_experiment_collection_metadata_encoder = SubExperimentCollectionMetadataCSVEncoder()
        self.sub_experiment_metadata_encoder = SubExperimentMetadataCSVEncoder()
        self.benchmark_observation_encoder = BenchmarkObservationCSVEncoder()
        self._encoders = []
        self._set_encoders()

    def _set_encoders(self):
        self._encoders =  [self.experiment_metadata_encoder,
                self.sub_experiment_collection_metadata_encoder,
                self.sub_experiment_metadata_encoder,
                self.benchmark_observation_encoder
                ]

    def encode_header(self):
        self._set_encoders()
        headers = []
        for encoder in self._encoders:
            headers.append(encoder.encode_header())
        return ','.join(headers)
        header = self._header
        return ','.join(header)

    def encode_body(self, o):
        self._set_encoders()
        body = []
        body.append(self.experiment_metadata_encoder.encode_body(o.experiment_metadata))
        body.append(self.sub_experiment_collection_metadata_encoder.encode_body(o.sub_experiment_collection_metadata))
        body.append(self.sub_experiment_metadata_encoder.encode_body(o.sub_experiment_metadata))
        body.append(self.benchmark_observation_encoder.encode_body(o.benchmark_observation))
        return ','.join(body)
