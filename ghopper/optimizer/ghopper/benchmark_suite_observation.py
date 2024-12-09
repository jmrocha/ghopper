from ghopper.benchmark_observation import BenchmarkObservation


class BenchmarkSuiteObservation:
    def __init__(self):
        self.suite_name: str = ""
        self.batch_max_length: int = -1
        self.batch_cardinality: int = -1
        self.benchmark_observation: BenchmarkObservation = BenchmarkObservation()

    def __repr__(self):
        return (
            "<BenchmarkSuiteObservation"
            f' "{self.suite_name=}"'
            f" {self.benchmark_observation=}"
            f" {self.batch_max_length=}"
            f" {self.batch_cardinality=}"
            ">"
        )
