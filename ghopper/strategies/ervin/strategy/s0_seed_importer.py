class S0SeedImporter:
    def from_string(self, sequences: str) -> set:
        phases = set()
        split = sequences.split("\n")
        sequences = filter(lambda x: len(x) > 1, split)
        for seq in sequences:
            seq = seq.split(":")[1]
            for phase in seq.split():
                phases.add(phase)
        return phases
