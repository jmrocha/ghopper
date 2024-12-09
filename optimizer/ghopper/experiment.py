from ghopper.benchmark_suite import BenchmarkSuite
from ghopper.experiment_observation import ExperimentObservation
from ghopper.experiment_metadata import ExperimentMetadata
from ghopper.benchmark_observation import BenchmarkObservation
from ghopper.sub_experiment_collection import SubExperimentCollection
import datetime


class Experiment:
    def __init__(self):
        self.benchmark_suite = BenchmarkSuite('.')
        self.sub_experiments: SubExperimentCollection = SubExperimentCollection()
        self.subscriber_callback = None
        self.datetime = datetime.datetime
        self.metadata = ExperimentMetadata()
        self._current_sub_experiment = None
        self.experiment_datetime = self.datetime.now()
        self.benchmark_timeout_in_s = 300

    def subscribe_observations(self, callback):
        self.subscriber_callback = callback

    def on_benchmark_observed(self, obs: BenchmarkObservation):
        obs = self._append_metadata(obs)
        if self.subscriber_callback:
            self.subscriber_callback(obs)

    def _append_metadata(self, obs: BenchmarkObservation) -> ExperimentObservation:
        experiment_obs = ExperimentObservation()
        experiment_obs = self._append_experiment_metadata(experiment_obs)
        experiment_obs = self._append_sub_experiment_collection_metadata(experiment_obs)
        experiment_obs = self._append_sub_experiment_metadata(experiment_obs)
        experiment_obs = self._append_experiment_metadata(experiment_obs)
        experiment_obs.benchmark_observation = obs
        
        return experiment_obs

    def _append_sub_experiment_collection_metadata(self, obs: ExperimentObservation):
        obs.sub_experiment_collection_metadata.requested_phase_order_lengths = self.sub_experiments.metadata.requested_phase_order_lengths
        obs.sub_experiment_collection_metadata.requested_phase_order_cardinalities= self.sub_experiments.metadata.requested_phase_order_cardinalities
        obs.sub_experiment_collection_metadata.strategy_seed= self.sub_experiments.metadata.strategy_seed
        obs.sub_experiment_collection_metadata.strategy= self.sub_experiments.metadata.strategy
        return obs

    def _append_sub_experiment_metadata(self, obs: ExperimentObservation):
        obs.sub_experiment_metadata.phase_order_max_length = self._current_sub_experiment.metadata.phase_order_max_length
        obs.sub_experiment_metadata.phase_order_cardinality = self._current_sub_experiment.metadata.phase_order_cardinality
        return obs

    def _append_experiment_metadata(self, obs: ExperimentObservation):
        self.metadata.experiment_datetime = self.experiment_datetime
        obs.experiment_metadata = self.metadata
        return obs


    def run(self):
        self.benchmark_suite.subscribe_observations(self.on_benchmark_observed)
        self.benchmark_suite.benchmark_timeout_in_s = self.benchmark_timeout_in_s
        for sub_experiment in self.sub_experiments:
            self._current_sub_experiment = sub_experiment
            for phase_order in sub_experiment:
                self.benchmark_suite.optimize(phase_order.sequence)
