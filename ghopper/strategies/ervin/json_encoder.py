from ervin.engine_result import *
from ervin.phase_sequence import PhaseSequence
import json


class ResultJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return {
            "parameters": ParametersJsonEncoder().default(o.parameters),
            "output": OutputJsonEncoder().default(o.output),
        }


class ParametersJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, EngineParameters):
            return {
                "length": o.length,
                "cardinality": o.cardinality,
                "strategy": o.strategy,
                "seed": o.seed,
            }
        return json.JSONEncoder.default(self, o)


class OutputJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, EngineOutput):
            return [OutputElementJsonEncoder().default(x) for x in o.output_elements]

        return json.JSONEncoder.default(self, o)


class OutputElementJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, EngineOutputElement):
            return {
                "metadata": MetadataJsonEncoder().default(o.metadata),
                "sequences": [
                    PhaseSequenceJsonEncoder().default(x) for x in o.sequences
                ],
            }

        return json.JSONEncoder.default(self, o)


class MetadataJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, EngineMetadata):
            return {"length": o.length, "cardinality": o.cardinality}
        return json.JSONEncoder.default(self, o)


class PhaseSequenceJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, PhaseSequence):
            return o.sequence
        return json.JSONEncoder.default(self, o)
