from ervin.graph.node import Node


class Edge:
    def __init__(self, node_from: Node, node_to: Node):
        self.node_from = node_from
        self.node_to = node_to
        self.counter = 1

    def increment_counter(self):
        self.counter += 1

    def get_weight(self):
        try:
            return self.counter / self.node_from.counter
        except ZeroDivisionError:
            return 0

    def __eq__(self, other):
        return (
            self.node_from == self.node_from
            and self.node_to == self.node_to
            and self.counter == other.counter
        )

    def __hash__(self):
        return hash((self.node_from, self.node_to))

    def __repr__(self):
        return (
            f"<Edge {self.node_from.name} -> {self.node_to.name} ({self.get_weight()})>"
        )
