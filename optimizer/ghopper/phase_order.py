import collections
import collections.abc


class PhaseOrder(collections.abc.Iterable):
    def __init__(self, sequence: str = ""):
        assert type(sequence) is str, (
            f"sequence needs to be of type {str}" f", but received {type(sequence)}"
        )

        self.sequence = sequence

    def __len__(self):
        return len(self.sequence.split(" "))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<PhaseOrder {self.sequence=}>"

    def __eq__(self, o):
        return isinstance(o, PhaseOrder) and self.sequence == o.sequence

    def __iter__(self):
        return iter(self.sequence)

    def __getitem__(self, key):
        return self.sequence.split()[key]

    def pair_iter(self) -> collections.abc.Iterator:
        return iter(PhaseOrderPairIterator(self.sequence))


class PhaseOrderPairIterator(collections.abc.Iterator):
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
