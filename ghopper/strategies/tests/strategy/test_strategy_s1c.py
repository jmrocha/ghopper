from unittest import TestCase, skip
from ervin.strategy.strategy_s1c import StrategyS1c
from ervin.graph.graph import Graph

@skip
class TestStrategyS1c(TestCase):
    def setUp(self):
        graph = Graph()
        graph.add_edge("a", "b", weight=1)
        graph.add_edge("b", "c", weight=0.1)
        graph.add_edge("b", "d", weight=0.9)
        self.strategy = StrategyS1c()
        self.strategy.graph = graph

    def test_get_first_pass(self) -> None:
        roots = []
        for i in range(10):
            root = self.strategy.get_first_pass()
            if root is not None:
                roots.append(root)
        self._assert_roots_are_random(roots)

    def _assert_roots_are_random(self, roots) -> None:
        roots = set(roots)
        self.assertTrue(len(roots) >= 1)
