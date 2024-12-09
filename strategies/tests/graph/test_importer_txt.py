from ervin.graph.importer_txt import ImporterTXT
from unittest import TestCase, skip


class TestImporterTXT(TestCase):
    @skip
    def test_get_sequences(self):
        importer = ImporterTXT(self.sequences_path)
        sequences = importer.get_sequences()
        expected_sequences = [["-a", "-b", "-c"], ["-a", "-b"]]
        self.assertEqual(sequences, expected_sequences)

    def test_from_string(self):
        txt = """
        a b
        d e
        """
        importer = ImporterTXT()
        sequences = importer.from_string(txt)
        self.assertEqual(sequences, [["a", "b"], ["d", "e"]])
