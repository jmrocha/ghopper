from ervin.graph.digraph import Digraph


class GraphBuilder:
    def __init__(self, sequences: list[list[str]]):
        self.sequences = sequences
        self.digraph = Digraph()

    def get_digraph(self) -> Digraph:
        for sequence in self.sequences:
            self.digraph.start_node(sequence[0])
            n = len(sequence) - 1
            for i in range(n):
                a, b = sequence[i], sequence[i + 1]
                self.digraph.add_edge(a, b)
        return self.digraph
