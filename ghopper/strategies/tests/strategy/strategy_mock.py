from ervin.strategy import Strategy
from ervin.phase_sequence import PhaseSequence
import random


class StrategyMock(Strategy):
    name = 'mock'
    def __init__(self):
        super().__init__()
        self.name = "mock"
        self.phases = ['a', 'b', 'c']

    def search(self) -> PhaseSequence:
        choices = random.choices(self.phases, k=self.sequence_length)
        choices = ' '.join(choices)
        return PhaseSequence(choices)
