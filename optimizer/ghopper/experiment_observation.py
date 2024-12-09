from ghopper.experiment_metadata import ExperimentMetadata
from ghopper.sub_experiment_collection_metadata import SubExperimentCollectionMetadata
from ghopper.sub_experiment_metadata import SubExperimentMetadata
from ghopper.benchmark_observation import BenchmarkObservation

class ExperimentObservation:
    def __init__(self):
        self.experiment_metadata = ExperimentMetadata()
        self.sub_experiment_collection_metadata = SubExperimentCollectionMetadata()
        self.sub_experiment_metadata = SubExperimentMetadata()
        self.benchmark_observation = BenchmarkObservation()
        

    def __repr__(self):
        return (
            "<ExperimentObservation"
            f" {self.experiment_metadata=}"
            f" {self.sub_experiment_collection_metadata=}"
            f" {self.sub_experiment_metadata=}"
            f" {self.benchmark_observation=}"
            ">"
        )
