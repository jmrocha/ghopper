from ghopper.phase_order import PhaseOrder


class SequenceImporter:
    def from_string(self, sequences: str) -> list[PhaseOrder]:
        split = sequences.split("\n")
        sequences = filter(lambda x: len(x) > 1, split)
        res = []
        for seq in sequences:
            sequence = []
            seq = seq.split(":")[1]
            sequence = " ".join(seq.split())
            res.append(PhaseOrder(sequence))

        return res
