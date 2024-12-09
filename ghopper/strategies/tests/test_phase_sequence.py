from ervin.phase_sequence import PhaseSequence, PhaseSequencePairIterator
from unittest import TestCase, skip


class TestPhaseSequence(TestCase):
    def test_iterable(self):
        seq = PhaseSequence("a b c")
        self.assertEqual(seq[0], "a")

    def test_pair_iterable(self):
        seq = PhaseSequence('a b c')
        (x,y),(u,v) = seq.pair_iter()
        self.assertEqual(x, 'a')
        self.assertEqual(y, 'b')
        self.assertEqual(u, 'b')
        self.assertEqual(v, 'c')

class TestPhaseSequencePairIterator(TestCase):
    def test_iter(self):
        iterator = PhaseSequencePairIterator('a b c')
        self.assertEqual(list(iter(iterator)),
                [('a', 'b'), ('b', 'c')])
