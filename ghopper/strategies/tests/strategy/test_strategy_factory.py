from ervin.strategy.strategy_factory import StrategyFactory
from ervin.strategy.strategy_s0 import StrategyS0
from ervin.graph.graph import Graph
from unittest import TestCase, skip
from ervin.strategy.s1_seed_importer import S1SeedImporter


class MockS1SeedImporter(S1SeedImporter):
    def __init__(self):
        super().__init__()
        self._from_string = None

    def return_from_string(self, value):
        self._from_string = value

    def from_string(self, value):
        return self._from_string

class MockS0SeedImporter(MockS1SeedImporter):
    pass

class TestStrategyFactory(TestCase):
    def setUp(self):
        self.factory = StrategyFactory()

    def test_strategies_available(self):
        l = self.factory.get_available_strategies()
        self.assertEqual(l, ["s0", "s1a", "s1b", "s1c"])

    def test_get_strategy(self):
        strategy = self.factory.get_strategy("s0")
        self.assertTrue(isinstance(strategy, StrategyS0))

    def test_seed(self):
        self.factory.seed = "Pass Arguments: i j k"
        strategy = self.factory.get_strategy("s0")
        self.assertEqual(set(strategy.phases), {"i", "j", "k"})
