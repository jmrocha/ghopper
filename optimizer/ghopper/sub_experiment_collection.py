from ghopper.sub_experiment import SubExperiment
from ghopper.sub_experiment_collection_metadata import SubExperimentCollectionMetadata
class SubExperimentCollection:
    def __init__(self, sub_experiments = None):
        self.metadata = SubExperimentCollectionMetadata()
        self._sub_experiments: list[SubExperiment] = []
        if sub_experiments:
             self._sub_experiments = sub_experiments

    def __iter__(self):
        return iter(self._sub_experiments)

    def __len__(self):
        return len(self._sub_experiments)

    def __getitem__(self, key):
        return self._sub_experiments[key]

    def append(self, sub_experiment: SubExperiment):
        self._sub_experiments.append(sub_experiment)

    def __repr__(self):
        return (
                '<SubExperimentCollection'
                f' {self.metadata=}'
                f' {self._sub_experiments=}'
                '>')
