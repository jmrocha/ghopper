class SubExperimentCollectionMetadata:
    def __init__(self):
        self.requested_phase_order_lengths: str = ''
        self.requested_phase_order_cardinalities: str = ''
        self.strategy: str = ''
        self.strategy_seed: str = ''

    def __repr__(self):
        return (
                '<SubExperimentCollectionMetadata'
                f' {self.requested_phase_order_lengths=}'
                f' {self.requested_phase_order_cardinalities=}'
                f' {self.strategy=}'
                f' {self.strategy_seed=}'
                '>')
