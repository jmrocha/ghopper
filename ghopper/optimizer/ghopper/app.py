from ghopper.engine_result_ui import EngineResultUI
from ghopper.experiment import Experiment, ExperimentMetadata
from ghopper.benchmark_suite import BenchmarkSuite
from ghopper.engine_result_json_decoder import EngineResultJsonDecoder
from ghopper.benchmark.error import *
from ghopper.experiment_observation_csv_encoder import ExperimentObservationCSVEncoder
from ghopper.sub_experiment_collection import SubExperimentCollection
from ghopper.sub_experiment import SubExperiment
from ghopper.phase_order import PhaseOrder
from ghopper.sub_experiment_collection_importer import SubExperimentCollectionImporter
from ghopper.engine_result_json_decoder import EngineResultJsonDecoder
from ghopper.util import Path
class App:
    def __init__(self):
        self.benchmark_suite_path = None
        self.phase_orders_path = None
        self.timeout_in_s = 300
        self.sample_size = 1
        self.output_path = 'out.csv'
        self.experiment_metadata = ExperimentMetadata()
        self.encoder = ExperimentObservationCSVEncoder()
        self.sub_experiments_importer = SubExperimentCollectionImporter()
        self.engine_result_importer = EngineResultJsonDecoder()
        self.print_header = True

    def run(self):
        experiment = self._get_experiment()
        experiment.benchmark_timeout_in_s = self.timeout_in_s
        print(self.encoder.encode_header())
        for i in range(self.sample_size):
            experiment.run()

    def _get_experiment(self):
        assert self.benchmark_suite_path
        assert self.phase_orders_path
        experiment = Experiment()
        experiment.benchmark_suite = BenchmarkSuite(self.benchmark_suite_path)
        experiment.subscribe_observations(self.on_experiment_observed)
        experiment.sub_experiments = self._get_sub_experiments()
        experiment.metadata = self.experiment_metadata
        return experiment

    def _get_sub_experiments(self):
        engine_result = None
        with open(self.phase_orders_path, 'r') as f:
            engine_result = self.engine_result_importer.decode(f.read())
        return self.sub_experiments_importer.from_engine_result(engine_result)

    def _get_mock_sub_experiments(self):
        sub_experiment = SubExperiment([PhaseOrder('-domtree')])
        sub_experiment.metadata.phase_order_max_length = 10000
        sub_experiment.metadata.phase_order_cardinality = 50000
        collection = SubExperimentCollection([sub_experiment])
        collection.metadata.requested_phase_order_lengths = 'requested_phase_order_lengths'
        collection.metadata.requested_phase_order_cardinalities = 'requested_phase_order_cardinalities'
        collection.metadata.strategy = 'strategy'
        collection.metadata.strategy_seed = 'strategy_seed'
        return collection

    def on_experiment_observed(self, obs):
        if Path(self.output_path).exists():
            self.print_header = False
        with open(self.output_path, 'a') as f:
            if self.print_header:
                header = self.encoder.encode_header()
                f.write(f'{header}\n')
                print(header)
                self.print_header = False
            encoded = self.encoder.encode_body(obs)
            f.write(f'{encoded}\n')
            print(encoded)
