from ervin.strategy.strategy_s0 import StrategyS0
from unittest import TestCase


class TestS0Strategy(TestCase):
    def setUp(self):
        self.strategy = StrategyS0()
        self.strategy.phases = ['a','b','c']

    def test_multiple_sequences(self):
        self.strategy.sequence_length = 5
        seq1 = self.strategy.search()
        seq2 = self.strategy.search()
        self.assertEqual(len(seq2), 5)

    def test_sequence_greater_than_phases(self):
        self.strategy.phases = ["a"]
        self.strategy.sequence_length = 3
        seq = self.strategy.search()
        self.assertEqual(len(seq), 3)
        self.assertEqual(set(seq.sequence.split()), {"a"})

    def test_sequence_of_10(self):
        self.strategy.phases = ['a','b']
        self.strategy.length = 10
        seq = self.strategy.search()
        self.assertEqual(10, len(seq))

    def test_randomness(self):
        self.strategy.phases = ['a','b','c']
        self.strategy.length = 50
        seq1 = self.strategy.search()
        seq2 = self.strategy.search()
        seq3 = self.strategy.search()
        self.assertNotEqual(seq1, seq2)
        self.assertNotEqual(seq1, seq3)
        self.assertNotEqual(seq2, seq3)
