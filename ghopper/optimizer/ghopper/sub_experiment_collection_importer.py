from ghopper.engine_result import EngineResult
from ghopper.sub_experiment_collection import SubExperimentCollection
from ghopper.sub_experiment import SubExperiment
from ghopper.phase_order_collection import PhaseOrderCollection

class SubExperimentCollectionImporter:
    def __init__(self):
        self.result = None
        self.sub_experiments = None

    def from_engine_result(self, result: EngineResult) -> SubExperimentCollection:
        self.result = result
        self.sub_experiments = SubExperimentCollection()
        self._set_experiment_metadata()
        self._set_sub_experiments()
        return self.sub_experiments

    def _set_experiment_metadata(self):
        self.sub_experiments.metadata.requested_phase_order_lengths = self.result.parameters.length
        self.sub_experiments.metadata.requested_phase_order_cardinalities = self.result.parameters.cardinality
        self.sub_experiments.metadata.strategy = self.result.parameters.strategy
        self.sub_experiments.metadata.strategy_seed = self.result.parameters.seed

    def _set_sub_experiments(self):
        for output_elem in self.result.output:
            sub_experiment = self._get_sub_experiment(output_elem)
            self.sub_experiments.append(sub_experiment)

    def _get_sub_experiment(self, output_elem):
        sub_experiment = SubExperiment()
        sub_experiment.metadata.phase_order_max_length = output_elem.metadata.length
        sub_experiment.metadata.phase_order_cardinality = output_elem.metadata.cardinality
        sub_experiment.phase_orders = PhaseOrderCollection(output_elem.sequences)
        return sub_experiment
