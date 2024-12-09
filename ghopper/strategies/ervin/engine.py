from ervin.engine_result import *
from ervin.phase_sequence import PhaseSequence
from ervin.util.range import Range
from ervin.strategy import Strategy


class Engine:
    def __init__(self):
        self.length: str = "10"
        self.cardinality: str = "1"
        self.strategy: Strategy = None
        self.seed: str = None
        self.current_length: int = -1
        self.current_cardinality: int = -1
        self.max_iterations = 15000 

    def get_sequence(self) -> PhaseSequence:
        self.strategy.sequence_length = self.current_length
        return self.strategy.search()

    def get_sequences(self) -> list[PhaseSequence]:
        res = set()
        i = 0
        while len(res) < self.current_cardinality and i < self.max_iterations:
            phase_order = self.get_sequence()
            res.add(phase_order)
            i += 1
        return list(res)

    def get_result(self) -> EngineOutputElement:
        res = EngineOutputElement()
        res.metadata = self.get_metadata()
        res.sequences = self.get_sequences()
        return res

    def get_metadata(self) -> EngineMetadata:
        metadata = EngineMetadata()
        metadata.length = self.current_length
        metadata.cardinality = self.current_cardinality
        return metadata

    def get_parameters(self) -> EngineParameters:
        parameters = EngineParameters()
        parameters.length = self.length
        parameters.cardinality = self.cardinality
        parameters.strategy = self.strategy.__class__.name
        parameters.seed = self.seed
        return parameters

    def run(self) -> EngineResult:
        res = EngineResult()
        res.parameters = self.get_parameters()
        cardinality = Range(self.cardinality)
        length = Range(self.length)
        while cardinality.has_next():
            self.current_cardinality = cardinality.next()
            while length.has_next():
                self.current_length = length.next()
                res.output.output_elements.append(self.get_result())
            length.reset()
        return res
