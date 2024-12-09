class ImporterTXT:
    def __init__(self, path: str = None):
        self.path = path

    def from_string(self, string: str) -> list[list[str]]:
        sequences = []
        y = filter(lambda x: len(x.split()) > 0, string.split("\n"))
        for x in y:
            sequences.append(x.split())
        return sequences

    def from_path(self, path: str) -> list[str]:
        self.path = path
        l = self.get_sequences()
        l2 = []
        for x in l:
            l2 += x
        return l2

    def get_sequences(self) -> list[list[str]]:
        sequences = []
        with open(self.path, "r") as f:
            for line in f:
                if self.is_line_valid(line):
                    sequence = self.get_sequence(line)
                    sequences.append(sequence)
        return sequences

    def is_line_valid(self, line: str) -> bool:
        return line != "" and line != "\n"

    def get_sequence(self, line: str) -> list[str]:
        # line: Pass Arguments: -a -b -c
        return line.split(":")[1].strip().split(" ")
