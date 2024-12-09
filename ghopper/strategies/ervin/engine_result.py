from ervin.phase_sequence import PhaseSequence
import collections


class EngineResult:
    def __init__(self):
        self.parameters: EngineParameters = EngineParameters()
        self.output: EngineOutput = EngineOutput()

    def __repr__(self):
        return (
            "<EngineResult\n"
            f"\tparameters={self.parameters}\n"
            f"\toutput={self.output}>"
        )


class EngineParameters:
    def __init__(self):
        self.length = None
        self.cardinality = None
        self.strategy = None
        self.seed = None

    def __repr__(self):
        return (
            "<EngineParameters"
            f" length={self.length}"
            f" cardinality={self.cardinality}"
            f" strategy={self.strategy}"
            ">"
        )


class EngineOutput(collections.abc.Sequence):
    def __init__(self):
        self.output_elements: list[EngineOutputElement] = []

    def __len__(self):
        return len(self.output_elements)

    def __iter__(self):
        return iter(self.output_elements)

    def __getitem__(self, key):
        return self.output_elements[key]

    def __repr__(self):
        return "<EngineOutput" f" elements={self.output_elements}" ">"


class EngineOutputElement:
    def __init__(self):
        self.metadata = EngineMetadata()
        self.sequences = []

    def __repr__(self):
        return (
            "<EngineOutputElement"
            f" metadata={self.metadata}"
            f" sequences={self.sequences}"
            ">"
        )


class EngineMetadata:
    def __init__(self):
        self.length = None
        self.cardinality = None

    def __repr__(self):
        return (
            "<EngineMetadata"
            f" length={self.length}"
            f" cardinality={self.cardinality}"
            ">"
        )


class EnginePhaseSequence:
    def __init__(self):
        self.sequences: list[str] = []
