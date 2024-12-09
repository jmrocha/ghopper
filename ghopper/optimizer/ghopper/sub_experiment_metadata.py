class SubExperimentMetadata:
    def __init__(self):
        self.phase_order_max_length: int = -1
        self.phase_order_cardinality: int = -1

    def __repr__(self):
        return (
                '<SubExperimentMetadata'
                f' {self.phase_order_max_length=}'
                f' {self.phase_order_cardinality=}'
                '>')
