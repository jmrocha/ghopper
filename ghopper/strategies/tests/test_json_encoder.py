from ervin.json_encoder import *
from ervin.engine_result import *
from ervin.phase_sequence import *
from unittest import TestCase, skip


class TestJsonEncoder(TestCase):
    def test_encode_parameters(self) -> None:
        encoder = ParametersJsonEncoder()
        result = EngineParameters()
        encoded = encoder.encode(result)
        data = json.loads(encoded)
        self.assertEqual(
            data, {"length": None, "cardinality": None, "strategy": None, "seed": None}
        )

    def test_encode_metadata(self) -> None:
        encoder = MetadataJsonEncoder()
        metadata = EngineMetadata()
        metadata.length = 10
        metadata.cardinality = 10
        encoded = encoder.encode(metadata)
        data = json.loads(encoded)
        self.assertEqual(data, {"length": 10, "cardinality": 10})

    def test_encode_output_element(self) -> None:
        encoder = OutputElementJsonEncoder()
        element = EngineOutputElement()
        encoded = encoder.encode(element)
        data = json.loads(encoded)
        self.assertEqual(
            data, {"metadata": {"length": None, "cardinality": None}, "sequences": []}
        )

    def test_encode_output(self) -> None:
        encoder = OutputJsonEncoder()
        output = EngineOutput()
        elem = EngineOutputElement()
        seq1 = PhaseSequence("a b c")
        seq2 = PhaseSequence("d e f")
        elem.sequences = [seq1, seq2]
        output.output_elements = [elem]
        encoded = encoder.encode(output)
        data = json.loads(encoded)
        expected = [
            {
                "metadata": {"length": None, "cardinality": None},
                "sequences": ["a b c", "d e f"],
            }
        ]
        self.assertEqual(data, expected)

    def test_encode_sequence(self) -> None:
        encoder = PhaseSequenceJsonEncoder()
        seq = PhaseSequence("a b c")
        encoded = encoder.encode(seq)
        data = json.loads(encoded)
        self.assertEqual(data, "a b c")

    def test_encode_result(self) -> None:
        encoder = ResultJsonEncoder()
        result = EngineResult()
        encoded = encoder.encode(result)
        data = json.loads(encoded)
        self.assertEqual(
            data,
            {
                "parameters": {
                    "length": None,
                    "cardinality": None,
                    "strategy": None,
                    "seed": None,
                },
                "output": [],
            },
        )
