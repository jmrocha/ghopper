from ghopper.engine_result import *
import json


class EngineResultJsonDecoder(json.JSONDecoder):
    def decode(self, s) -> EngineResult:
        data = json.loads(s)
        res = EngineResult()
        parameters = data.get("parameters")
        output = data.get("output")
        res.parameters = EngineParametersDecoder().decode(parameters)
        res.output = EngineOutputDecoder().decode(output)
        return res


class EngineParametersDecoder:
    def decode(self, o) -> EngineParameters:
        parameters = EngineParameters()
        parameters.length = o.get("length")
        parameters.cardinality = o.get("cardinality")
        parameters.strategy = o.get("strategy")
        parameters.seed = o.get("seed")
        return parameters


class EngineMetadataDecoder:
    def decode(self, o) -> EngineMetadata:
        metadata = EngineMetadata()
        metadata.length = o.get("length")
        metadata.cardinality = o.get("cardinality")
        return metadata


class EnginePhaseOrderDecoder:
    def decode(self, o) -> EnginePhaseOrder:
        sequence_elem = EnginePhaseOrder()
        sequence_elem.sequences = [PhaseOrder(x) for x in o]
        return sequence_elem


class EngineOutputElementDecoder:
    def decode(self, o) -> EngineOutputElement:
        elem = EngineOutputElement()
        elem.metadata = EngineMetadataDecoder().decode(o.get("metadata"))
        elem.sequences = EnginePhaseOrderDecoder().decode(o.get("sequences"))
        return elem


class EngineOutputDecoder:
    def decode(self, o) -> EngineOutput:
        output = EngineOutput()
        elems = [EngineOutputElementDecoder().decode(x) for x in o]
        output.output_elements = elems
        return output
