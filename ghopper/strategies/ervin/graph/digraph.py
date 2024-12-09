import networkx as nx
from ervin.graph.edge import Edge
from ervin.graph.node import Node
import json


class Digraph:
    def __init__(self):
        self._nodes = {}
        self.edges = {}
        self._start_counter = {}
        # self._graph = pgv.AGraph(directed=True)
        self._graph = nx.DiGraph()

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, g):
        self._graph = g
        self._start_counter = json.loads(g.graph_attr["start-counter"])

    def add_node(self, key: str, value: any) -> None:
        self._nodes[key] = value

    def add_edge(self, a: str, b: str, **kwarg):
        self._graph.add_edge(a, b, **kwarg)
        if self.has_edge(a, b):
            edge = self.get_edge(a, b)
            edge.increment_counter()
            edge.node_from.increment_counter()
        else:
            if self.has_node(a):
                node_a = self.get_node(a)
            else:
                node_a = Node(a)

            if self.has_node(b):
                node_b = self.get_node(b)
            else:
                node_b = Node(b)

            edge = Edge(node_a, node_b)
            node_a.increment_counter()
            self.edges[hash(edge)] = edge
            self._nodes[node_a.name] = node_a
            self._nodes[node_b.name] = node_b

    def has_edge(self, a: str, b: str):
        edge = Edge(Node(a), Node(b))
        return hash(edge) in self.edges

    def get_edge(self, a: str, b: str):
        edge = Edge(Node(a), Node(b))
        return self.edges[hash(edge)]

    def get_node(self, name: str):
        return self._nodes[name]

    def has_node(self, name: str):
        return name in self._nodes

    def __eq__(self, other) -> int:
        return self._nodes == other._nodes and self.edges == other.edges

    def __hash__(self) -> int:
        return hash((self._nodes, self.edges))

    def __repr__(self) -> str:
        return f"<Digraph nodes={list(self._nodes.values())} edges={list(self.edges.values())}>"

    def start_node(self, node):
        try:
            old_counter = self._start_counter[node]
            self._start_counter[node] = old_counter + 1
        except KeyError:
            self._start_counter[node] = 1

    def successors(self, node: Node) -> list[Node]:
        return list(self._graph.successors(node))

    def out_edges_iter(self, node: Node):
        return self._graph.out_edges(node)

    def get_edge_weight(self, edge):
        return self._graph.edges[edge]["label"]

    def in_edges(self, node: Node):
        return self._graph.in_edges(node)

    def nodes(self):
        return self._graph.nodes()

    def get_starting_nodes(self):
        return dict(self._start_counter.items())

    def node_with_higher_indegree(self):
        return max(self._graph.in_degree(), key=lambda x: x[1])[0]
