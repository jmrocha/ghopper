from ervin.phase_sequence import PhaseSequence


class SequenceImporter:
    def from_string(self, sequences: str) -> list[PhaseSequence]:
        split = sequences.split("\n")
        sequences = filter(lambda x: len(x) > 1, split)
        res = []
        for seq in sequences:
            sequence = []
            seq = seq.split(":")[1]
            sequence = " ".join(seq.split())
            res.append(PhaseSequence(sequence))

        return res
