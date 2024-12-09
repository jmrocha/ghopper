from ervin.strategy.strategy_s0 import StrategyS0
from ervin.strategy.strategy_s1a import StrategyS1a
from ervin.strategy.strategy_s1b import StrategyS1b
from ervin.strategy.strategy_s1c import StrategyS1c
from ervin.strategy.s0_seed_importer import S0SeedImporter
from ervin.strategy.s1_seed_importer import S1SeedImporter


class StrategyFactory:
    def __init__(self):
        self._strategies = {
            StrategyS0.name: (StrategyS0, S0SeedImporter),
            StrategyS1a.name: (StrategyS1a, S1SeedImporter),
            StrategyS1b.name: (StrategyS1b, S1SeedImporter),
            StrategyS1c.name: (StrategyS1c, S1SeedImporter),
        }
        self.seed = None

    def get_available_strategies(self):
        return list(self._strategies.keys())

    def get_strategy(self, name):
        strategy, importer = self._strategies[name]
        strategy, importer = strategy(), importer()
        if self.seed:
            if isinstance(strategy, StrategyS1a):
                strategy.graph = importer.from_string(self.seed)
            elif isinstance(strategy, StrategyS0):
                strategy.phases = importer.from_string(self.seed)
        return strategy
