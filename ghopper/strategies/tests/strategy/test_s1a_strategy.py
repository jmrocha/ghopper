from unittest import TestCase
from ervin.strategy.strategy_s1a import StrategyS1a
from ervin.graph.graph import Graph


class TestS1aStrategy(TestCase):
    def setUp(self):
        graph = Graph()
        graph.add_edge("a", "b", weight=1)
        graph.add_edge("b", "c", weight=0.9)
        self.strategy = StrategyS1a()
        self.strategy.graph = graph

    def test_get_sequence(self):
        sequence = self.strategy.search()
        condition = sequence.sequence == "b c" or sequence == "b a"
        self.assertTrue(condition)

    def test_length(self):
        graph = Graph()
        graph.add_edge("a", "b", weight=1)
        graph.add_edge("b", "a", weight=1)
        self.strategy.graph = graph
        self.strategy.sequence_length = 25
        sequences = [len(self.strategy.search()) for x in range(10)]
        max_len = max(sequences)
        self.assertEqual(max_len, 25)
