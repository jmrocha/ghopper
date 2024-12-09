import datetime
class ExperimentMetadata:
    def __init__(self):
        self.experiment_datetime = datetime.datetime.now()
        self.toolchain = ''
        self.target = ''
        self.dataset_size = ''
        self.benchmark_suite_name = ''

    def __repr__(self):
        return (
                '<ExperimentMetadata'
                f' {self.experiment_datetime=}'
                f' {self.toolchain=}'
                f' {self.dataset_size=}'
                f' {self.benchmark_suite_name=}'
                '>'
                )
