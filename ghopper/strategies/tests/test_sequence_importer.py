from ervin.sequence_importer import SequenceImporter
from ervin.phase_sequence import PhaseSequence
from unittest import TestCase


class TestSequenceImporter(TestCase):
    def test_from_string(self):
        importer = SequenceImporter()
        sequences = importer.from_string("Pass Arguments: a b c")
        self.assertEqual(sequences, [PhaseSequence("a b c")])
