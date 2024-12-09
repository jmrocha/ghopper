from ghopper.engine_result import EngineResult
from ghopper.engine_result_json_decoder import *
from unittest import TestCase, skip
import json


class TestEngineResultJsonDecoder(TestCase):
    def setUp(self):
        pass

    def test_decode_parameters(self):
        data = {"length": "10", "cardinality": "1", "strategy": "s0", "seed": None}
        decoder = EngineParametersDecoder()
        parameters = decoder.decode(data)
        self.assertEqual(parameters.length, "10")
        self.assertEqual(parameters.cardinality, "1")
        self.assertEqual(parameters.strategy, "s0")
        self.assertEqual(parameters.seed, None)

    def test_decode_metadata(self):
        data = {"length": 1, "cardinality": 2}
        metadata = EngineMetadataDecoder().decode(data)
        self.assertEqual(metadata.length, 1)
        self.assertEqual(metadata.cardinality, 2)

    def test_decode_sequences(self):
        data = ["a b c", "d e f"]

        sequence_elem = EnginePhaseOrderDecoder().decode(data)
        self.assertEqual(len(sequence_elem), 2)
        self.assertEqual(len(sequence_elem[0]), 3)

    def test_decode_output_elem(self):
        data = {
            "metadata": {"length": 10, "cardinality": 2},
            "sequences": ["a b c", "d e f"],
        }
        output_elem = EngineOutputElementDecoder().decode(data)
        self.assertEqual(output_elem.metadata.length, 10)
        self.assertEqual(len(output_elem.sequences[0]), 3)

    def test_decode_output(self):
        data = [{"metadata": {"length": 1}, "sequences": ["a b"]}]
        output = EngineOutputDecoder().decode(data)
        self.assertEqual(output[0].metadata.length, 1)
        self.assertEqual(len(output), 1)

    def test_decode_result(self):
        data = {
            "parameters": {"length": "10"},
            "output": [{"metadata": {}, "sequences": []}],
        }
        json_str = json.dumps(data)
        res = EngineResultJsonDecoder().decode(json_str)
        self.assertEqual(res.parameters.length, "10")
        self.assertEqual(len(res.output[0].sequences), 0)
