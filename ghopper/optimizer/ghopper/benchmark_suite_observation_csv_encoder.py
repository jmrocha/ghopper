from ghopper.benchmark_observation_csv_encoder import BenchmarkObservationCSVEncoder
class BenchmarkSuiteObservationCSVEncoder:
    def __init__(self):
        self.benchmark_observation_encoder = BenchmarkObservationCSVEncoder()
        self._header = [
                'benchmark_suite','batch_max_length', 'batch_cardinality'
                ]

    def encode_header(self) -> str:
        benchmark_header = self.benchmark_observation_encoder.encode_header()
        header = self._header + [benchmark_header]
        return ','.join(header)

    def encode_body(self, o) -> str:
        bsuite = [str(x) for x in [o.suite_name, o.batch_max_length, o.batch_cardinality]]
        benchmark = [self.benchmark_observation_encoder.encode_body(o.benchmark_observation)]
        body = bsuite + benchmark
        return ','.join(body)
