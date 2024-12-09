from ervin.strategy import Strategy


class GraphSearch:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def get_sequence(self) -> list[str]:
        sequence = []
        while self.strategy.has_next_pass():
            next_pass = self.strategy.next_pass()
            sequence.append(next_pass)
        return sequence
