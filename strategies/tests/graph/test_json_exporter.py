from ervin.graph.json_exporter import JsonExporter
from ervin.graph.digraph import Digraph
from unittest import TestCase


class TestJsonExporter(TestCase):
    def test_to_json(self):
        exporter = JsonExporter()
        graph = Digraph()
        graph.add_edge("a", "b", weight=1)
        data = exporter.to_json(graph)
        self.assertEqual(data["links"][0]["weight"], 1)
