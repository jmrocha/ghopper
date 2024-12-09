from ervin.graph.json_importer import JsonImporter
from unittest import TestCase
import json

class TestJsonImporter(TestCase):
    def test_from_string(self):
        importer = JsonImporter()
        data = {
          "directed": True,
          "multigraph": False,
          "graph": {},
          "nodes": [
            {
              "id": "a"
            },
            {
              "id": "b"
            }
          ],
          "links": [
            {
              "weight": 1.0,
              "source": "a",
              "target": "b"
            }
          ]
        }
        data_string = json.dumps(data)
        graph = importer.from_string(data_string)
        self.assertEqual(graph.edges['a','b']['weight'], 1.0)
