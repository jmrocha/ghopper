class BenchmarkSuiteConfig:
    def __init__(self):
        self.path: str = '.'
        self.benchmark_timeout_in_s: float = 300 # five minutes
