import matplotlib.pyplot as plt

"""
    CPU Cycles Speedup per Benchmark against the best result.
    This is shown as a boxplot.
"""


class Plot1:
    def __init__(self):
        self.title = "Comparison against the best result"
        self.xlabel, self.x = "Benchmark", "benchmark"
        self.ylabel, self.y = "CPU cycles speedup", "cpu_cycles"
        self.data = None
        self.fig = None
        self.ax = None

    def draw(self):
        self.ax.boxplot(self.data.cpu_cycles_speedup, labels=self.data.benchmarks)
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
