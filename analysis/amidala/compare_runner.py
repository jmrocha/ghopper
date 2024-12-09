from amidala.experiment import Experiment
from amidala.experiment_compare import ExperimentCompare
from amidala.experiment_factory import ExperimentFactory
from amidala.statistics import Statistics
from amidala.dataframe_cache import DataFrameCache
from amidala.data import Data
from amidala.myplot import MyPlot
from amidala.util import Util
import matplotlib.pyplot as plt
import calendar,time
import pandas as pd

class CompareRunner:
    def run(self):
        self.df = self.get_df()
        speedups = self.get_speedups()
        benchmarks = self._get_benchmarks(self.benchmarks)
        self.plot(speedups, benchmarks)

    def __init__(self):
        self.db = ''
        self.candidate = ''
        self.baseline = ''
        self.benchmarks = ''
        self.title = ''
        self.save_path = ''
        self.sharex = False
        self.show = False
        self.plotname = ''
        self._stats = Statistics()
        self._data = Data()
        self._cache = DataFrameCache()

    def get_df(self):
        cache_path = f'.cache/{self.db}.pkl'
        if self._cache.exists(cache_path):
            return self._cache.get(cache_path)
        else:
            df = self._data.get(self.db)
            self._cache.df = df
            self._cache.save(cache_path)
            return df

    def get_speedups(self):
        cache_path = f'.cache/speedups-{self.candidate}{self.baseline}.pkl'
        if self._cache.exists(cache_path):
            return self._cache.get(cache_path)
        else:
            factory = ExperimentFactory()
            factory.df = self.df
            candidate = factory.get(self.candidate)
            baseline = factory.get(self.baseline)
            speedups = candidate.compare(baseline)
            self._cache.df = speedups
            self._cache.save(cache_path)
            return speedups
        
    def plot(self, speedups, benchmarks):
        if self.plotname == 'box':
            self._plot_speedups(speedups, benchmarks)
        elif self.plotname == 'bar':
            self._bar(speedups, benchmarks)

    def _bar(self, speedups, benchmarks):
        plot = MyPlot()
        if self.benchmarks != '':
            plot.benchmarks = benchmarks
        fig, ax = plt.subplots(1,
                figsize=Util().set_size(426.79135))
        plot.ax = ax
        import matplotlib.ticker as mtick
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        plot.title = self.title
        plot.ylabel = 'CPU Cycles Reduction'
        df = 1/speedups.cpu_cycles
        df = 1 - df
        df *= 100
        df = df.T
        plot.bar(df)
        if self.show:
            plt.show()
        if self.save_path != '':
            fig.savefig(f"{self.save_path}.pgf", bbox_inches="tight")

    def _get_benchmarks(self,benchmarks):
        if benchmarks != '':
            benchmarks = benchmarks.split(',')
        return benchmarks

    def _plot_speedups(self,speedups,benchmarks):
        plot = MyPlot()
        if self.benchmarks != '':
            plot.benchmarks = benchmarks
        fig, axs = plt.subplots(2, sharex=self.sharex,
                figsize=Util().set_size(426.79135, subplots=(2,1)))
        plot.ax = axs[0]
        import matplotlib.ticker as mtick
        axs[0].yaxis.set_major_formatter(mtick.PercentFormatter())
        plot.title = self.title
        plot.ylabel = 'CPU Cycles Reduction'
        df = 1/speedups.cpu_cycles
        df = 1 - df
        df *= 100
        plot.plot(df)
        axs[1].yaxis.set_major_formatter(mtick.PercentFormatter())
        plot.ax = axs[1]
        plot.xlabel = 'Benchmark'
        plot.ylabel = 'Code Size Reduction'
        df = 1/speedups.code_size_in_bytes
        df = 1 - df
        df *= 100
        plot.plot(df)
        if self.show:
            plt.show()
        #timestamp = calendar.timegm(time.gmtime())
        #path = f'{timestamp}'
        if self.save_path != '':
            fig.savefig(f"{self.save_path}.pgf", bbox_inches="tight")
