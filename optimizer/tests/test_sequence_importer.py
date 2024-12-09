from ghopper.sequence_importer import SequenceImporter
from ghopper.phase_order import PhaseOrder
from unittest import TestCase


class TestSequenceImporter(TestCase):
    def test_from_string(self):
        importer = SequenceImporter()
        sequences = importer.from_string("Pass Arguments: a b c")
        self.assertEqual(sequences, [PhaseOrder("a b c")])
