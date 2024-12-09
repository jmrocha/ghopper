from .strategy_s1a import StrategyS1a
from random import SystemRandom


class StrategyS1b(StrategyS1a):
    name = "s1b"

    def __init__(self):
        super().__init__()
        self.name = "s1b"
        self.random = SystemRandom()

    def get_first_pass(self):
        nodes = list(self.graph.nodes)
        return self.random.choice(nodes)
