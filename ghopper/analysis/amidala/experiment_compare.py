from amidala.experiment_factory import ExperimentFactory
from amidala.dataframe_cache import DataFrameCache
from amidala.statistics import Statistics
from amidala.data import Data
import hashlib

class ExperimentCompare:
    def __init__(self):
        self.db_path = ''
        self._cache = DataFrameCache()
        self._stats = Statistics()
        self._data = Data()
        self._df = None

    def _pre_process_db(self):
        cache_path = f'.cache/{self.db_path}.pkl'
        if self._cache.exists(cache_path): 
            df = self._cache.get(cache_path)
        else:
            df = self._data.get(self.db_path)
            df = self._data.rename_df(df)
            df = self._data.hash(df)
            df = self._data.columns_df(df)
            self._cache.df = df
            self._cache.save(cache_path)
        return df

    def _get_speedups(self, candidate_df,baseline_df,cache_path):
        if self._cache.exists(cache_path): 
            speedups = self._cache.get(cache_path)
        else:
            speedups = self._stats.compare(candidate_df, baseline_df)
            self._cache.df = speedups
            self._cache.save(cache_path)
        return speedups

    def _get_baseline(self, baseline):
        factory = ExperimentFactory()
        factory.df = self.df
        experiment = factory.get(baseline)
        experiment.init()
        return experiment

    def _get_candidate(self, candidate):
        factory = ExperimentFactory()
        factory.df = self.df
        experiment = factory.get(candidate)
        experiment.init()
        return experiment

    def _get_speedups_cache_path(self, baseline,candidate):
        name = hashlib.md5(str((baseline,candidate)).encode()).hexdigest()
        return f'.cache/{name}.pkl'

    def get_speedups(self, candidate, baseline):
        # todo: add cache here
        self.df = self._pre_process_db()
        baseline = self._get_baseline(baseline)
        candidate = self._get_candidate(candidate)
        return candidate.compare(baseline)
        cache_path = self._get_speedups_cache_path(baseline,candidate)
        return self._get_speedups(candidate_df,baseline_df,cache_path)
