from __future__ import annotations
import networkx as nx
import collections


class Graph:
    def __init__(self):
        self._graph = nx.DiGraph()

    def add_edge(self, a: any, b: any, **kwords) -> None:
        self._graph.add_edge(a, b, **kwords)

    def successors(self, source: any) -> collections.abc.Iterable:
        return list(self._graph.successors(source))

    def out_edges_iter(self, source: any) -> collections.abc.Iterable:
        return self._graph.out_edges(source)

    def get_edge_weight(self, edge) -> float:
        a,b = edge
        return self._graph.edges[a, b]["weight"]

    def node_with_higher_indegree(self):
        return max(self._graph.in_degree(), key=lambda x: x[1])[0]

    def in_edges(self, node: any):
        return self._graph.in_edges(node)


    def out_degree(self, source: any, weight_label: str):
        return self._graph.out_degree(source, weight_label)

    def has_edge(self, a: any, b: any) -> bool:
        return self._graph.has_edge(a,b)

    def update(self, edges=None, nodes=None) -> None:
        return self._graph.update(edges=edges,nodes=nodes)

    def _getedges(self) -> collections.abc.Iterable:
        return self._graph.edges

    def _getnodes(self) -> collections.abc.Iterable:
        return self._graph.nodes

    def _setgraph(self, graph: Graph) -> None:
        self._graph = graph

    def starting_nodes(self) -> set:
        pass

    def copy(self):
        return self._graph.copy()

    edges = property(fget=_getedges)
    nodes = property(fget=_getnodes)
    graph = property(fset=_setgraph)
