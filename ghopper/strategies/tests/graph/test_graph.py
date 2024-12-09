from ervin.graph.graph import Graph
from unittest import TestCase


class TestGraph(TestCase):
    def setUp(self):
        self.g = Graph()

    def test_add_edge(self):
        self.g.add_edge(1, 2, weight=2)
        self.assertEqual(len(self.g.edges), 1)
        self.assertEqual(self.g.edges[1,2]['weight'], 2)

    def test_successors(self):
        self.g.add_edge(1, 2)
        successors = self.g.successors(1)
        self.assertEqual(len(list(successors)), 1)

    def test_out_edges_iter(self):
        self.g.add_edge(1, 2)
        out_edges = self.g.out_edges_iter(1)
        self.assertEqual(len(out_edges), 1)

    def test_get_edge_weight(self):
        self.g.add_edge(1, 2, weight=0.2)
        weight = self.g.get_edge_weight((1,2))
        self.assertEqual(weight, 0.2)

    def test_node_with_higher_indegree(self):
        self.g.add_edge(1, 2)
        self.g.add_edge(3, 2)
        higher = self.g.node_with_higher_indegree()
        self.assertEqual(higher, 2)

    def test_in_edges(self):
        self.g.add_edge(1, 2)
        self.g.add_edge(3, 2)
        in_edges = self.g.in_edges(2)
        self.assertEqual(len(in_edges), 2)
