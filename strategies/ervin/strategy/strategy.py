from ervin.phase_sequence import PhaseSequence


class Strategy:
    def __init__(self):
        self.sequence_length = 10
        self.max_iterations = 10000
        self.name: str = ''

    def has_next_pass(self) -> bool:
        raise NotImplementedError

    def next_pass(self) -> str:
        raise NotImplementedError

    def search(self) -> PhaseSequence:
        passes = []
        while self.has_next_pass():
            passes.append(self.next_pass())
        self._reset()
        return PhaseSequence(" ".join(passes))

    def _reset(self):
        pass
