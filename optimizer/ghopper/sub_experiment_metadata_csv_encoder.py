class SubExperimentMetadataCSVEncoder:
    def __init__(self):
        self._header = ['phase_order_max_length','phase_order_cardinality']

    def encode_header(self):
        return ','.join(self._header)

    def encode_body(self, o):
        body = [str(x) for x in [o.phase_order_max_length, o.phase_order_cardinality]]
        return ','.join(body)
