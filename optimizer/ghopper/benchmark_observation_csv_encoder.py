from ghopper.metrics_csv_encoder import MetricsCSVEncoder


class BenchmarkObservationCSVEncoder:
    def __init__(self):
        self.metrics_encoder = MetricsCSVEncoder()
        self._header = [
            "name",
            "sequence_requested",
            "sequence_executed",
            'has_error',
            'error'
        ]

    def encode_header(self) -> str:
        metrics_header = [self.metrics_encoder.encode_header()]
        header = self._header + metrics_header
        return ",".join(header)

    def encode_body(self, o) -> str:
        assert o.sequence_requested
        assert o.sequences_executed
        sequences_executed = ";".join([x.sequence for x in o.sequences_executed])

        benchmark_data = [o.name, o.sequence_requested.sequence, sequences_executed, str(o.has_error), f'"{o.error}"']
        benchmark = ",".join(benchmark_data).encode('unicode_escape').decode('utf-8')
        metrics = self.metrics_encoder.encode_body(o.metrics)
        return f"{benchmark},{metrics}"
