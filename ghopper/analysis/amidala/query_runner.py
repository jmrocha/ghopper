from amidala.dataframe_cache import DataFrameCache
from amidala.data import Data
from amidala.experiment_factory import ExperimentFactory
import pandas as pd

class QueryRunner:
    def run(self):
        assert self.db is not None, 'CSV path is not defined'
        self.df = self.get_df()
        speedups = self.get_speedups()
        reduction = self.get_reduction_from_speedups(speedups)
        breakpoint()

    def get_reduction_from_speedups(self, speedups):
        speedups = speedups.copy()
        speedups = 1 / speedups
        speedups = 1 - speedups
        speedups *= 100
        return speedups

    def get_df_by_id(self, id):
        factory = ExperimentFactory()
        factory.df = self.df
        return factory.get(id)._df

    def get_uniq_phases(self, df):
        orders = []
        phases = []

        sequences = df.sequence_executed
        for s in sequences:
            for x in s.split(';'):
                orders.append(x)
        for x in orders:
            for y in x.split():
                phases.append(y)
        return list(set(phases))

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
            speedups = candidate.compare_without_pivot(baseline)
            speedups = speedups.apply(pd.to_numeric,errors='ignore') 
            self._cache.df = speedups
            self._cache.save(cache_path)
            return speedups

    def __init__(self):
        self.db = None
        self.df = None
        self.candidate = None
        self.baseline = None
        self._cache = DataFrameCache()
        self._data = Data()
