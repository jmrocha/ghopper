from ervin.graph.graph_importer import GraphImporter
from ervin.graph.graph import Graph
from unittest import TestCase, skip


class TestGraphImporter(TestCase):
    def setUp(self):
        self.importer = GraphImporter()
    def test_import_from_string(self):
        graph = self.importer.from_string(
                "Pass Arguments: a b\n"
                "Pass Arguments: a b\n"
                "Pass Arguments: b c\n"
                "Pass Arguments: b d"
                )
        self.assertEqual(graph.edges['a','b']['weight'], 1.0)
        self.assertEqual(graph.edges['b','c']['weight'], 0.5)
        self.assertEqual(graph.edges['b','d']['weight'], 0.5)

    def test_weights_normalized(self):
        graph = self.importer.from_string(
                'pass arguments: a b\n'
                'pass arguments: b c\n'
                'pass arguments: b c\n'
                'pass arguments: b c\n'
                'pass arguments: b d\n'
                'pass arguments: b d\n'
                'pass arguments: b e\n'
                )
        self.assertEqual(1.0, graph.edges['a', 'b']['weight'])
        self.assertEqual(3/6, graph.edges['b', 'c']['weight'])
        self.assertEqual(2/6, graph.edges['b', 'd']['weight'])
        self.assertEqual(1/6, graph.edges['b', 'e']['weight'])
