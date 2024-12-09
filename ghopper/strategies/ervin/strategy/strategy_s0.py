from ervin.strategy import Strategy
from ervin.phase_sequence import PhaseSequence
import random


class StrategyS0(Strategy):
    name = "s0"

    def search(self) -> PhaseSequence:
        try:
            random_phases = random.choices(self.phases, k=self.sequence_length)
            random_phases = ' '.join(random_phases)
        except IndexError:
            random_phases = ''
        return PhaseSequence(random_phases)

    def __init__(self):
        super().__init__()
        self.phases = []
