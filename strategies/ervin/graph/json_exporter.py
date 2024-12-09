from ervin.graph.digraph import Digraph
import networkx as nx


class JsonExporter:
    def to_json(self, graph: Digraph) -> dict:
        return nx.node_link_data(graph._graph)
