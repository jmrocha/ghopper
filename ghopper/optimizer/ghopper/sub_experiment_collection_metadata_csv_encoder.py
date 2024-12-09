class SubExperimentCollectionMetadataCSVEncoder:
    def __init__(self):
        self._header = ['requested_phase_order_lengths','requested_phase_order_cardinalities','strategy','strategy_seed']

    def encode_header(self):
        return ','.join(self._header)

    def encode_body(self, o):
        if o.strategy_seed is None:
            o.strategy_seed = 'N/A'
        body = [f'"{o.requested_phase_order_lengths}"',f'"{o.requested_phase_order_cardinalities}"',
                o.strategy,o.strategy_seed]
        return ','.join(body)
