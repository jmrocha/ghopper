from ervin.graph.graph import Graph 
import networkx as nx
import json


class JsonImporter:
    def from_string(self, graph_json: str) -> Graph:
        graph = json.loads(graph_json)
        g = nx.node_link_graph(graph)
        res = Graph()
        res.graph = g
        return res
