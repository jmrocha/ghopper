from .strategy import Strategy
import random
from ervin.graph.graph import Graph
from ervin.graph.range import Range
from ervin.graph.json_importer import JsonImporter


class StrategyS1a(Strategy):
    name = "s1a"

    def __init__(self):
        super().__init__()
        self.name = "s1a"
        self.graph: Graph = self._get_o0_graph()
        self.current_iteration = 0
        self.current_sequence_length = 0

    def _get_o0_graph(self) -> Graph:
        o0_string = '{"directed": true, "multigraph": false, "graph": {}, "nodes": [{"id": "-tti"}, {"id": "-verify"}, {"id": "-ee-instrument"}, {"id": "-targetlibinfo"}, {"id": "-assumption-cache-tracker"}, {"id": "-profile-summary-info"}, {"id": "-annotation2metadata"}, {"id": "-forceattrs"}, {"id": "-basiccg"}, {"id": "-always-inline"}, {"id": "-barrier"}, {"id": "-annotation-remarks"}], "links": [{"weight": 0.5, "source": "-tti", "target": "-verify"}, {"weight": 0.5, "source": "-tti", "target": "-assumption-cache-tracker"}, {"weight": 1.0, "source": "-verify", "target": "-ee-instrument"}, {"weight": 1.0, "source": "-targetlibinfo", "target": "-tti"}, {"weight": 1.0, "source": "-assumption-cache-tracker", "target": "-profile-summary-info"}, {"weight": 1.0, "source": "-profile-summary-info", "target": "-annotation2metadata"}, {"weight": 1.0, "source": "-annotation2metadata", "target": "-forceattrs"}, {"weight": 1.0, "source": "-forceattrs", "target": "-basiccg"}, {"weight": 1.0, "source": "-basiccg", "target": "-always-inline"}, {"weight": 1.0, "source": "-always-inline", "target": "-barrier"}, {"weight": 1.0, "source": "-barrier", "target": "-annotation-remarks"}, {"weight": 1.0, "source": "-annotation-remarks", "target": "-verify"}]}'
        return JsonImporter().from_string(o0_string)

    def search(self):
        self.current_node = self.get_first_pass()
        return super().search()

    def _reset(self):
        self.current_iteration = 0
        self.current_sequence_length = 0

    def has_next_pass(self):
        return (
            not self.has_reached_max_iterations()
            and (self.has_successors() or self.is_first_iteration())
            and not self.has_reached_desired_sequence_length()
        )

    def is_first_iteration(self):
        return self.current_iteration == 0

    def has_reached_max_iterations(self):
        return self.current_iteration >= self.max_iterations

    def has_successors(self):
        return (
            self.current_iteration == 0
            or len(self.graph.successors(self.current_node)) > 0
        )

    def has_reached_desired_sequence_length(self):
        return self.current_sequence_length >= self.sequence_length

    def next_pass(self) -> str:
        self.current_iteration += 1
        self.current_sequence_length += 1
        if self.current_iteration == 1:
            return self.current_node

        random = self.get_random()
        probability_distribution = self.get_probability_distribution()
        assert (
            len(probability_distribution) > 0
        ), "Probability distribution needs at least one interval"
        # todo: we choose at least the first node,
        # but the node should always be explicitly chosen by the probability distribution
        node = probability_distribution[0].node
        for interval in probability_distribution:
            if random in interval:
                node = interval.node
                self.current_node = node
                break

        assert node != "", "No interval was selected from the probability distribution"
        self.current_node = node
        return node

    def get_probability_distribution(self) -> list[Range]:
        distribution = []
        current_weight = 0
        edges = list(self.graph.out_edges_iter(self.current_node))
        assert (
            len(edges) > 0
        ), "There should be at least one outgoing edge from the current node"
        for edge in edges:
            interval = Range()
            interval.a = current_weight
            interval.b = current_weight + self.get_edge_weight(edge)
            current_weight = interval.b
            interval.node = edge[1]
            interval.a /= 10
            interval.b /= 10
            distribution.append(interval)
        return distribution

    def get_random(self) -> float:
        return random.random()

    def get_edge_weight(self, edge):
        return self.graph.get_edge_weight(edge)

    def get_first_pass(self) -> str:
        assert self.graph, 'Graph was not set'
        return self.graph.node_with_higher_indegree()

    def get_conn_degree(self, node: str) -> float:
        return sum([float(x.attr["label"]) for x in self.graph.in_edges(node)])
