class BenchmarkError(Exception):
    pass


class BenchmarkCompileError(BenchmarkError):
    pass


class BenchmarkOptimizeError(BenchmarkError):
    pass


class BenchmarkTimeoutError(BenchmarkError):
    pass
