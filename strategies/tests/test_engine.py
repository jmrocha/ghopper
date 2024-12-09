from ervin.engine import Engine
from tests.strategy.strategy_mock import StrategyMock
from unittest import TestCase, skip


class TestEngine(TestCase):
    def setUp(self):
        self.engine = Engine()
        self.engine.strategy = StrategyMock()

    def test_engine_output_length(self):
        self.engine.length = "1"
        self.engine.cardinality = "2"
        result = self.engine.run()
        self.assertEqual(1, len(result.output))

    def test_engine_parameters(self):
        self.engine.length = "[10,20]"
        self.engine.cardinality = "2"
        self.engine.seed = "seed"
        result = self.engine.run()
        parameters = result.parameters
        self.assertEqual(parameters.length, "[10,20]")
        self.assertEqual(parameters.cardinality, "2")
        self.assertEqual(parameters.strategy, "mock")
        self.assertEqual(parameters.seed, "seed")

    def test_engine_output_metadata(self):
        self.engine.length = "10"
        self.engine.cardinality = "2"
        self.engine.seed = "seed"
        result = self.engine.run()
        metadata = result.output[0].metadata
        self.assertEqual(metadata.length, 10)
        self.assertEqual(metadata.cardinality, 2)

    def test_output_multiple_length_and_cardinality(self):
        self.engine.length = "1,2"
        self.engine.cardinality = "1,2"
        result = self.engine.run()
        self.assertEqual(type(result.output[0].sequences), list)
        self.assertEqual(len(result.output[1].sequences), 2)
        self.assertEqual(len(result.output), 4)
