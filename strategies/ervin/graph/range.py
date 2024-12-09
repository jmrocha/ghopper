class Range:
    def __init__(self):
        self.a = -1.0
        self.b = -1.0
        self.node = "n/a"

    def __repr__(self):
        return f"<Range [{self.a}, {self.b}[ node: {self.node}>"

    def __contains__(self, item: float) -> bool:
        return item >= self.a and item < self.b
