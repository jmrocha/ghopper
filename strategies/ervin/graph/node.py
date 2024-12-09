class Node:
    def __init__(self, name: str):
        self.name = name
        self.counter = 0

    def increment_counter(self):
        self.counter += 1

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Node {self.name}({self.counter})>"
