from ghopper.engine_result_json_decoder import EngineResultJsonDecoder
class EngineResultUI:
    def __init__(self, path):
        self.sequences_path = path

    def print(self):
        data = self._get_data()
        print(
            "--------------\n"
            "Requested data\n"
            "--------------\n"
            f'\tlength="{data.parameters.length}",'
            f'\n\tcardinality="{data.parameters.cardinality}",'
            f"\n\tstrategy={data.parameters.strategy}"
        )
        print("---------\n" "Sequences" "\n---------")
        for elem in data.output:
            length = elem.metadata.length
            cardinality = elem.metadata.cardinality
            print(f"\t{cardinality} sequences of length {length}:")
            for i, sequence in enumerate(elem):
                print(f"\t\t{i + 1}: {sequence.sequence}")

    def _get_data(self):
        decoder = EngineResultJsonDecoder()
        with open(self.sequences_path, "r") as f:
            return decoder.decode(f.read())
