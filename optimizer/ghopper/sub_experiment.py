from ghopper.phase_order_collection import PhaseOrderCollection
from ghopper.sub_experiment_metadata import SubExperimentMetadata

class SubExperiment:
    def __init__(self, phase_order_collection = PhaseOrderCollection()):
        self.phase_orders: PhaseOrderCollection = phase_order_collection 
        self.metadata = SubExperimentMetadata()

    def __iter__(self):
        return iter(self.phase_orders)

    def __repr__(self):
        return (
                '<SubExperiment'
                f' {self.phase_orders=}'
                f' {self.metadata=}'
                '>')
