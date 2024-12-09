from ghopper.experiment import Experiment
from ghopper.metrics import Metrics
from ghopper.experiment_runner import ExperimentRunner
from ghopper.benchmark_observation import BenchmarkObservation
from ghopper.experiment_observation import ExperimentObservation
from ghopper.benchmark_suite_config import BenchmarkSuiteConfig
from ghopper.sub_experiment import SubExperiment
from ghopper.phase_order_collection import PhaseOrderCollection
from ghopper.phase_order import PhaseOrder
from ghopper.sub_experiment_collection import SubExperimentCollection
from tests.mock_benchmark_suite import MockBenchmarkSuite
from tests.mock_benchmark import MockBenchmark
from tests.mock_datetime import MockDatetime
from unittest import TestCase, skip
import datetime

class TestExperiment(TestCase):
    def setUp(self):
        self.mock_bsuite = MockBenchmarkSuite()
        self.experiment = Experiment()
        self.experiment.benchmark_suite = self.mock_bsuite
        self.experiment.metadata.benchmark_suite_name = 'suite X'
        self.experiment.metadata.requested_length = '10,20'
        self.experiment.metadata.requested_cardinality = '2,4'
        self.experiment.metadata.seed_description = 'seed'
        self.experiment.metadata.strategy = 's0'
        sub_experiment = SubExperiment(PhaseOrderCollection([PhaseOrder('a b')]))
        self.experiment.sub_experiments = SubExperimentCollection([sub_experiment])
        self.mock_callback = MockCallback()
        sub_experiment = SubExperiment()
        self.experiment._current_sub_experiment = sub_experiment

    def test_subscribe_and_optimize(self):
        self.experiment.run()
        self.assertEqual('subscribe optimize', self.mock_bsuite.get_log())

    def test_push_observation(self):
        self.experiment.subscribe_observations(self.mock_callback.on_benchmark_observed)
        self.experiment.on_benchmark_observed(BenchmarkObservation())
        self.assertEqual('on_benchmark_observed', self.mock_callback.log) 

    def test_append_experiment_metadata(self):
        self.experiment.experiment_datetime = datetime.datetime(year=2021, month=1, day=1)
        self.experiment.metadata.toolchain = 'toolchain'
        self.experiment.metadata.target = 'target'
        self.experiment.metadata.dataset_size = 'size'
        self.experiment.metadata.benchmark_suite_name = 'suite'
        self.experiment.subscribe_observations(self.mock_callback.on_benchmark_observed)
        self.experiment.on_benchmark_observed(BenchmarkObservation())
        self.assertEqual(datetime.datetime(year=2021, month=1, day=1), self.mock_callback.observation.experiment_metadata.experiment_datetime)
        self.assertEqual('toolchain', self.mock_callback.observation.experiment_metadata.toolchain)
        self.assertEqual('target', self.mock_callback.observation.experiment_metadata.target)
        self.assertEqual('size', self.mock_callback.observation.experiment_metadata.dataset_size)
        self.assertEqual('suite', self.mock_callback.observation.experiment_metadata.benchmark_suite_name)


    def test_append_sub_experiments_metadata(self):
        obs = BenchmarkObservation()
        self.experiment.sub_experiments.metadata.requested_phase_order_lengths = '10,20'
        self.experiment.sub_experiments.metadata.requested_phase_order_cardinalities = '2,4'
        self.experiment.sub_experiments.metadata.strategy = 's0'
        self.experiment.sub_experiments.metadata.strategy_seed = 'seed'
        self.experiment.subscribe_observations(self.mock_callback.on_benchmark_observed)
        self.experiment.on_benchmark_observed(obs)
        self.assertEqual('10,20', self.mock_callback.observation.sub_experiment_collection_metadata.requested_phase_order_lengths)
        self.assertEqual('2,4', self.mock_callback.observation.sub_experiment_collection_metadata.requested_phase_order_cardinalities)
        self.assertEqual('seed', self.mock_callback.observation.sub_experiment_collection_metadata.strategy_seed)
        self.assertEqual('s0', self.mock_callback.observation.sub_experiment_collection_metadata.strategy)

    def test_append_sub_experiment_metadata(self):
        obs = BenchmarkObservation()
        sub_experiment = SubExperiment()
        sub_experiment.metadata.phase_order_max_length = 10
        sub_experiment.metadata.phase_order_cardinality = 20
        self.experiment._current_sub_experiment = sub_experiment
        self.experiment.subscribe_observations(self.mock_callback.on_benchmark_observed)
        self.experiment.on_benchmark_observed(obs)
        self.assertEqual(10, self.mock_callback.observation.sub_experiment_metadata.phase_order_max_length)
        self.assertEqual(20, self.mock_callback.observation.sub_experiment_metadata.phase_order_cardinality)


    def test_append_benchmark_observation(self):
        obs = BenchmarkObservation()
        obs.benchmark_name = 'gemm'
        self.experiment.subscribe_observations(self.mock_callback.on_benchmark_observed)
        self.experiment.on_benchmark_observed(obs)
        self.assertEqual('gemm', self.mock_callback.observation.benchmark_observation.benchmark_name)


class MockCallback:
    def __init__(self):
        self.observation = ExperimentObservation()
        self.log = ''

    def on_benchmark_observed(self, obs: ExperimentObservation):
        self.log += 'on_benchmark_observed'
        self.observation = obs
