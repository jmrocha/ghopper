from ervin.graph.graph_builder import GraphBuilder
from ervin.graph.digraph import Digraph
from ervin.graph.edge import Edge
from ervin.graph.node import Node
from unittest import TestCase


class TestGraphBuilder(TestCase):
    def test_get_graph(self):
        sequences = [["a", "b", "c"], ["b", "c"], ["b", "d"]]
        builder = GraphBuilder(sequences)
        graph = builder.get_digraph()
        expected_digraph = self.get_expected_digraph()
        self.assertEqual(graph, expected_digraph)

    def get_expected_digraph(self):
        digraph = Digraph()
        digraph._nodes = self.get_expected_nodes()
        digraph.edges = self.get_expected_edges()
        return digraph

    def get_expected_nodes(self):
        node_a = Node("a")
        node_b = Node("b")
        node_c = Node("c")
        node_d = Node("d")
        node_a.counter = 1
        node_b.counter = 3
        node_c.counter = 0
        node_d.counter = 0
        return {
            "a": node_a,
            "b": node_b,
            "c": node_c,
            "d": node_d,
        }

    def get_expected_edges(self):
        nodes = self.get_expected_nodes()
        node_a = nodes["a"]
        node_b = nodes["b"]
        node_c = nodes["c"]
        node_d = nodes["d"]
        edge1 = Edge(node_a, node_b)
        edge2 = Edge(node_b, node_c)
        edge3 = Edge(node_b, node_d)
        edge2.counter = 2
        return {hash(edge1): edge1, hash(edge2): edge2, hash(edge3): edge3}

    def test_start_counter(self):
        sequences = [["a", "b", "c"], ["b", "c"], ["b", "d"]]
        builder = GraphBuilder(sequences)
        graph = builder.get_digraph()
        expected_start_counter = {"a": 1, "b": 2}
        self.assertEqual(graph.get_starting_nodes(), expected_start_counter)
