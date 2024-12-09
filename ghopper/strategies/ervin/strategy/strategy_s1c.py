from .strategy_s1a import StrategyS1a


class StrategyS1c(StrategyS1a):
    name = "s1c"

    def __init__(self):
        super().__init__()
        self.name = "s1c"

    def get_first_pass(self):
        nodes_set = self.graph.starting_nodes()
        return nodes_set.pop()
