from ghopper.phase_order import PhaseOrder, PhaseOrderPairIterator
from unittest import TestCase, skip


class TestPhaseOrder(TestCase):
    def test_iterable(self):
        seq = PhaseOrder("a b c")
        self.assertEqual(seq[0], "a")

    def test_pair_iterable(self):
        seq = PhaseOrder("a b c")
        (x, y), (u, v) = seq.pair_iter()
        self.assertEqual(x, "a")
        self.assertEqual(y, "b")
        self.assertEqual(u, "b")
        self.assertEqual(v, "c")


class TestPhaseOrderPairIterator(TestCase):
    def test_iter(self):
        iterator = PhaseOrderPairIterator("a b c")
        self.assertEqual(list(iter(iterator)), [("a", "b"), ("b", "c")])
