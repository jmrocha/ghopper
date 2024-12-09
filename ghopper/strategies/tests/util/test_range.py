from ervin.util.range import Range
from unittest import TestCase


class TestRange(TestCase):
    def test_single_number(self):
        r = Range("10")
        self.assertEqual(list(r), [10])

    def test_range(self):
        r = Range("[1, 2]")
        self.assertEqual(list(r), [1, 2])

    def test_range_with_step(self):
        r = Range("[10, 20], 5")
        self.assertEqual(list(r), [10, 15, 20])

    def test_sequence(self):
        r = Range("10,15,20")
        self.assertEqual(list(r), [10, 15, 20])

    def test_iter(self):
        r = Range("[1,5]")
        count = 0
        for i in r:
            count += 1
        self.assertEqual(count, 5)

    def test_bad_interval(self):
        self.assertRaises(AttributeError, lambda: Range("[1,"))

    def test_random(self):
        # generate two random values between 1 and 10
        r = Range(f"[1,10],random,2")
        self.assertTrue(r.has_next())
        l1 = [r.next(), r.next()]
        self.assertFalse(r.has_next())
        self.assertEqual(len(set(l1)), 2)
        r.reset()
        l2 = [r.next(), r.next()]
        self.assertEqual(l1, l2)

    def test_random_n_is_char(self):
        self.assertRaises(AttributeError, lambda: Range("[1,10],random,a"))

    def test_bad_random_n_is_invalid_int(self):
        self.assertRaises(AttributeError, lambda: Range("[1,10],random,11"))
