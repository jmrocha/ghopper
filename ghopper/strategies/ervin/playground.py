import json


class Data:
    def __init__(self):
        self.parameters = Parameters()
        self.output = Output()


class Parameters:
    def __init__(self):
        self.length = None


class Output:
    def __init__(self):
        self.outputs: list[Sequence] = []


class Sequence:
    def __init__(self):
        self.metadata = Metadata()


class Metadata:
    def __init__(self):
        self.length = None


class DataJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Data):
            return {
                "parameters": ParametersJsonEncoder().default(o),
                "output": OutputJsonEncoder().default(o),
            }
        return json.JSONEncoder.default(self, o)


class ParametersJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return {"length": "10, 20", "cardinality": "1"}


class OutputJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return ["a"]


data = Data()
data.parameters.length = "10"
encoder = DataJsonEncoder(indent=2)
encoded = encoder.encode(data)
print(encoded)
