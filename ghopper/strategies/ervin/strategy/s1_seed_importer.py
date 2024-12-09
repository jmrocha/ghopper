from ervin.graph.digraph import Digraph
from ervin.graph.json_importer import JsonImporter


class S1SeedImporter:
    def from_string(self, graph_json: str) -> Digraph:
        return JsonImporter().from_string(graph_json)
