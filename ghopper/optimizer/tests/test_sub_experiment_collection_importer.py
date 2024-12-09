from ghopper.engine_result import EngineResult, EngineOutputElement
from ghopper.sub_experiment_collection_importer import SubExperimentCollectionImporter
from ghopper.phase_order_collection import PhaseOrderCollection
from ghopper.phase_order import PhaseOrder
from unittest import TestCase, skip
class TestSubExperimentCollectionImporter(TestCase):
    def setUp(self):
        self.importer = SubExperimentCollectionImporter()
        self.engine_result = self._get_engine_result()

    def _get_engine_result(self):
        self.engine_result = EngineResult()
        self._set_engine_parameters()
        self._set_output_elements()
        return self.engine_result

    def _set_output_elements(self):
        phase_orders = [PhaseOrder('a b')]
        elem1 = self._get_engine_output_element(10,20, phase_orders)
        elem2 = self._get_engine_output_element(40, 70, phase_orders)
        self.engine_result.output.output_elements = [elem1, elem2]


    def _get_engine_output_element(self, length, cardinality, phase_orders):
        elem = EngineOutputElement()
        elem.metadata.length = length
        elem.metadata.cardinality = cardinality
        elem.sequences.sequences = phase_orders
        return elem

    def _set_engine_parameters(self):
        self.engine_result.parameters.length = '10,20' 
        self.engine_result.parameters.cardinality = '20,40'
        self.engine_result.parameters.strategy = 's0'
        self.engine_result.parameters.seed = 'seed'

    def test_import_experiment_metadata_from_engine_result(self):
        sub_experiments = self.importer.from_engine_result(self.engine_result)
        self.assertEqual('10,20', sub_experiments.metadata.requested_phase_order_lengths)
        self.assertEqual('20,40', sub_experiments.metadata.requested_phase_order_cardinalities)
        self.assertEqual('s0', sub_experiments.metadata.strategy)
        self.assertEqual('seed', sub_experiments.metadata.strategy_seed)

    def test_import_sub_experiments(self):
        sub_experiments = self.importer.from_engine_result(self.engine_result)
        self.assertEqual(2, len(sub_experiments))
        self.assertEqual(40, sub_experiments[1].metadata.phase_order_max_length)
        self.assertEqual(70, sub_experiments[1].metadata.phase_order_cardinality)
        self.assertEqual(PhaseOrder('a b'), sub_experiments[1].phase_orders[0])
