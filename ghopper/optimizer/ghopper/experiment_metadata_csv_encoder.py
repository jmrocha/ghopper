from ghopper.experiment_metadata import ExperimentMetadata
class ExperimentMetadataCSVEncoder:
    def __init__(self):
        self._header = ['experiment_datetime', 'toolchain', 'target', 'dataset_size',
                'benchmark_suite_name']

    def encode_header(self):
        return ','.join(self._header)

    def encode_body(self, o):
        assert type(o) is ExperimentMetadata
        values = [str(o.experiment_datetime),o.toolchain,o.target,o.dataset_size,
                o.benchmark_suite_name]
        return ','.join(values)
