import collections


class PhaseSequence(collections.abc.Iterable):
    def __init__(self, seq: str = ""):
        assert type(seq) is str
        self.sequence = seq

    def __len__(self):
        return len(self.sequence.split(" "))

    def __hash__(self):
        return hash(self.sequence)

    def __str__(self):
        return self.sequence

    def __repr__(self):
        return self.sequence

    def __eq__(self, o):
        return isinstance(o, PhaseSequence) and self.sequence == o.sequence

    def __iter__(self):
        return iter(self.sequence)

    def __getitem__(self, key):
        return self.sequence.split()[key]

    def pair_iter(self) -> collections.abc.Iterator:
        return iter(PhaseSequencePairIterator(self.sequence))

class PhaseSequencePairIterator(collections.abc.Iterator):
    def __init__(self, sequence: str):
        self.sequence: list[str] = sequence.split()
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx == len(self.sequence) - 1:
            raise StopIteration
        res = self.sequence[self.idx], self.sequence[self.idx + 1]
        self.idx += 1
        return res

