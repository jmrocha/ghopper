from ghopper.phase_order import PhaseOrder
import collections


class EngineResult:
    def __init__(self):
        self.parameters: EngineParameters = EngineParameters()
        self.output: EngineOutput = EngineOutput()

    def __repr__(self):
        return (
            "<EngineResult\n"
            f"\tparameters={self.parameters}\n"
            f"\toutput=\n\t\t{self.output}>"
        )


class EngineParameters:
    def __init__(self):
        self.length = None
        self.cardinality = None
        self.strategy = None
        self.seed = None

    def __eq__(self, o):
        return (
            self.length == o.length
            and self.cardinality == o.cardinality
            and self.strategy == o.strategy
            and self.seed == o.seed
        )

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
        return "<EngineOutput" f" elements=\n\t\t\t{self.output_elements}" ">"

    def __eq__(self, o):
        return self.output_elements == o.output_elements


class EngineOutputElement:
    def __init__(self):
        self.metadata = EngineMetadata()
        self.sequences = EnginePhaseOrder()

    def __iter__(self):
        return iter(self.sequences)

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

    def __eq__(self, o):
        return self.length == o.length and self.cardinality == o.cardinality


class EnginePhaseOrder:
    def __init__(self):
        self.sequences: list[PhaseOrder] = []

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, key):
        return self.sequences[key]

    def __eq__(self, o):
        return self.sequences == o.sequences

    def __repr__(self):
        return f"<EnginePhaseOrder sequences=[{self.sequences}]>"
