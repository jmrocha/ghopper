from unittest import TestCase
from ervin.strategy.s0_seed_importer import S0SeedImporter


class TestS0SeedImporter(TestCase):
    def setUp(self):
        self.importer = S0SeedImporter()

    def test_import_phases(self) -> None:
        phases: set = self.importer.from_string(
            "Pass Arguments:a b c\n" "Pass Arguments:c d e"
        )
        self.assertEqual(phases, {"a", "b", "c", "c", "d", "e"})

    def test_import_phases_extra_spaces(self) -> None:
        phases: set = self.importer.from_string(
            "\n" "  " "Pass Arguments:  a b c\n" "Pass Arguments: c d e" "   " "\n"
        )
        self.assertEqual(phases, {"a", "b", "c", "c", "d", "e"})

    def test_import_single_sequence(self) -> None:
        phases = self.importer.from_string("Pass Arguments: a b c")
        self.assertEqual(phases, {"a", "b", "c"})
