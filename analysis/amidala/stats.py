from scipy.stats import gmean
import pandas as pd
from pathlib import Path
from util import Util
import hashlib
import itertools


class Stats:
    def compute_samples_median(self, df: pd.DataFrame) -> pd.DataFrame:
        #assert df.columns[0][0] == 'metrics', "metrics needs to be the first column in df"
        assert len(df.index.names) == 6, 'df needs to have a multi-index of 6 levels'

        res = []
        for _, group in df.groupby(level=[0,1,2,3,4,5]):
            df_median = self._compute_samples_median(group)
            res.append(df_median)
        return pd.concat(res)

    def _compute_samples_median(self, df: pd.DataFrame) -> pd.DataFrame:
        assert 'metadata' in df, '"metadata" needs to be a column in df'
        assert len(df.index.names) == 6, 'df needs to have a multi-index of 6 levels'

        df_copy = df[['metrics']].groupby(level=[0,1,2,3,4,5]).median()
        df_metadata = df.loc[:, ['metadata']].drop_duplicates()
        return df_copy.join(df_metadata)

    def concat_geometric_mean(self, df: pd.DataFrame) -> pd.DataFrame:
        assert df.columns[0][0] == 'metrics', "metrics needs to be the first column in df"
        assert len(df.index.names) == 6, 'df needs to have a multi-index of 6 levels'

        res = []
        for _, group in df.groupby(level=[0,1,2,3,4]):
            df_gmean = self._get_geometric_mean(group)
            res.append(df_gmean)
        return pd.concat(res)

    def _get_geometric_mean(self, df: pd.DataFrame) -> pd.DataFrame:
        assert df.columns[0][0] == 'metrics', "metrics needs to be the first column in df"
        assert len(df.index.names) == 6, 'df needs to have a multi-index of 6 levels'
        assert {'date', 'strategy', 'length', 'cardinality', 'phases', 'bench'}.issubset(df.index.names)
        #assert len(set(df.reset_index().phases_requested_id)) == 1

        metrics_avg = df[['metrics']].aggregate([gmean]).rename(index={'gmean':'_average'})
        df2 = df.iloc[[0]]
        idx = df2.index[0][5]
        df2 = df2.rename(index={idx:'_average'}, level=5)
        df2 = pd.concat([df, df2])
        df2 = df2.reset_index().set_index('bench')
        df2.loc[['_average'], ['metrics']] = metrics_avg

        return (
                df2
                .reset_index()
                .set_index(
                    ['date', 'strategy', 'length',
                     'cardinality', 'phases', 'bench'
                    ])
                )

    def _compare_benchmark_suites(self, baseline, candidate):
        import pdb; pdb.set_trace()
        assert 'metrics' in baseline
        assert 'metrics' in candidate
        #assert len(baseline) == len(set(baseline.bench))
        #assert len(candidate) == len(set(candidate.bench))

        baseline = baseline.reset_index().set_index("bench")[['metrics']]
        candidate = candidate.reset_index().set_index("bench")[['metrics']]
        df = baseline.join(candidate, lsuffix="_baseline", rsuffix="_candidate")
        speedups_df = df.metrics_baseline / df.metrics_candidate
        speedups_df.columns = pd.MultiIndex.from_product([['metrics_speedups'], list(speedups_df.columns)])
        df = df.join(speedups_df)
        return df[['metrics_speedups']]

    def compare_experiments(self, df1, df2):
        # todo: assert that df1 (baseline) cannot have more than 1 sub-experiment
        obs_list = [] 
        for _, group in df2.groupby(level=[0,1,2,3]):
            df = self._compare_benchmark_suites(df1, group)
            obs = group.join(df)
            obs_list.append(obs)
        res = pd.concat(obs_list)
        return (
                res
                .reset_index()
                .set_index(['strategy', 'length',
                     'cardinality', 'phases', 'bench' ])
                [['metrics_speedups']]
                )

    def compare(self, baseline, candidate):
        baseline = baseline.reset_index().set_index("bench")[['metrics']]
        candidate = candidate.reset_index().set_index("bench")[['metrics']]
        df = baseline.join(candidate, lsuffix="_baseline", rsuffix="_candidate")
        speedups_df = df.metrics_baseline / df.metrics_candidate
        speedups_df.columns = pd.MultiIndex.from_product([['metrics_speedups'], list(speedups_df.columns)])
        return speedups_df[['metrics_speedups']]
        df = df.join(speedups_df)
        return df


    def myinit(self):
        self.df = pd.read_csv(self.data_path,na_values='None')
        self.df = self.pre_process_df(self.df)

    def __init__(self, data_path=None):
        self.data_path = data_path
        self.df = None
        self.baseline_id = None
        self.candidate_id = None
        self.baseline = None
        self.candidate = None
        self.util = Util()

    def index_df(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.set_index(
                ['date','strategy','length',
                'cardinality','phases','bench',
                ])

    def columns_df(self, df: pd.DataFrame) -> pd.DataFrame:
        metrics_tuples = (
                list(itertools.product(['metrics'],df.iloc[:,10:].columns))
                )
        metadata_tuples = (
                list(itertools.product(['metadata'],df.iloc[:,:10].columns))
                )
        tuples = metadata_tuples + metrics_tuples
        df.columns = pd.MultiIndex.from_tuples(tuples)
        return df

    def create_sequence_hash(self, df):
        import hashlib
        df.loc[:, ['phases']] = df.apply(lambda x: hashlib.sha1(x.phases.encode()).hexdigest(), axis=1)
        df.loc[:, ['sequence_executed']] = df.apply(lambda x: hashlib.sha1(x.sequence_executed.encode()).hexdigest(), axis=1)
        return df

    def create_date_hash(self, df):
        import hashlib
        df.loc[:, ['date']] = df.apply(lambda x: hashlib.sha1(x.date.encode()).hexdigest(), axis=1)
        return df

    def pre_process_df(self, df):
        df = df.query('has_error == "False"')
        df = self.rename_df(df)
        df = self.create_sequence_hash(df)
        df = self.create_date_hash(df)
        df = self.index_df(df)
        df = self.columns_df(df)
        return df

    def rename_df(self, df):
        return df.rename(columns={
            'experiment_datetime': 'date',
            'requested_phase_order_lengths': 'length',
            'requested_phase_order_cardinalities': 'cardinality',
            'sequence_requested': 'phases',
            'name': 'bench'
            })
    def from_csv(self, path):
        return pd.read_csv(path)

    """
    ------------8<---------------- 
    """

    def concat_gmean(self, df: pd.DataFrame):
        df_gmean = df.loc[:, ["suite_id", "cpu_cycles"]].groupby("suite_id").agg(gmean)
        df_metadata = df.drop_duplicates(subset="suite_id").set_index("suite_id")
        df = df.set_index("suite_id")
        del df_metadata["cpu_cycles"]
        del df_metadata["measurement_id"]
        df_gmean = df_gmean.join(df_metadata)
        df_gmean.loc[:, "benchmark"] = "!ALL"
        # todo: replace hash with sha-1 for coherence
        df_gmean.loc[:, "measurement_id"] = df_gmean.apply(
            lambda x: hash(
                (
                    x.benchmark_suite,
                    x.strategy,
                    x.length,
                    x.cardinality,
                    x.phases_requested_id,
                    x.benchmark,
                )
            ),
            axis=1,
        )
        df = pd.concat([df, df_gmean])
        return df.reset_index()

    def get_ids(self):
        df = self.df.drop_duplicates(subset="experiment_id")
        fields = [
            "experiment_id",
            "strategy",
            "cardinality",
            "length",
            "dataset_size",
            "sample_size",
        ]
        return df.loc[:, fields].set_index("experiment_id")

    def get_speedups(self):
        self.baseline = self._get_experiment(self.baseline_id)
        self.candidate = self._get_experiment(self.candidate_id)
        return self._get_speedups()

    def get_speedups_against_best_standard_opt(self):
        self.baseline = self.get_std_opts()
        self.candidate = self._get_experiment(self.candidate_id)
        self.baseline = self._get_best_baseline()
        return self._get_speedups()

    def _get_best_baseline(self):
        return self.baseline.groupby("benchmark", as_index=False).min()

    def _get_experiment(self, id):
        return self.df.query(f'experiment_id == "{id}"')

    def _get_speedups(self):
        candidate = self.candidate
        baseline = self.baseline
        speedups = (
            candidate.set_index("benchmark")
            .loc[:, ["measurement_id", "cpu_cycles"]]
            .join(
                baseline.set_index("benchmark").loc[
                    :, ["measurement_id", "cpu_cycles"]
                ],
                rsuffix="_baseline",
            )
        )
        speedups["speedup"] = speedups.cpu_cycles_baseline / speedups.cpu_cycles
        speedups = speedups.reset_index().set_index("measurement_id")
        del speedups["cpu_cycles"]
        del speedups["cpu_cycles_baseline"]
        del speedups["benchmark"]
        return candidate.set_index("measurement_id").merge(
            speedups, left_index=True, right_index=True
        )

    def init(self):
        if self._has_cache():
            self.df = self._read_cache()
        else:
            self._write_cache()

    def _has_cache(self):
        return Path(f"{self.data_path}.pkl").exists()

    def _read_cache(self):
        return pd.read_pickle(f"{self.data_path}.pkl")

    def _write_cache(self):
        self.df = pd.read_csv(self.data_path).query("has_error == False")
        self.df.loc[:, "experiment_id"] = self.df.apply(
            lambda x: x.experiment_id[:7], axis=1
        )
        self._filter_median()
        self._concat_gmean()
        self.df.to_pickle(f"{self.data_path}.pkl")

    def _filter_median(self):
        df_median = self.df.groupby("measurement_id").median()
        df_uniq = self.df.drop_duplicates(subset="measurement_id").set_index(
            "measurement_id"
        )
        df_uniq.update(df_median)
        self.df = df_uniq.reset_index()

    def _concat_gmean(self):
        df_gmean = (
            self.df.loc[:, ["suite_id", "cpu_cycles"]].groupby("suite_id").agg(gmean)
        )
        df_metadata = self.df.drop_duplicates(subset="suite_id").set_index("suite_id")
        self.df = self.df.set_index("suite_id")
        del df_metadata["cpu_cycles"]
        del df_metadata["measurement_id"]
        df_gmean = df_gmean.join(df_metadata)
        df_gmean.loc[:, "benchmark"] = "!ALL"
        # replace hash with sha-1 for coherence
        df_gmean.loc[:, "measurement_id"] = df_gmean.apply(
            lambda x: hash(
                (
                    x.benchmark_suite,
                    x.strategy,
                    x.length,
                    x.cardinality,
                    x.phases_requested_id,
                    x.benchmark,
                )
            ),
            axis=1,
        )
        self.df = pd.concat([self.df, df_gmean])
        self.df = self.df.reset_index()

    def get_std_opts(self):
        return self.df.loc[self.df.strategy.str.startswith("-O")]

    def get_std_opts_speedups(self):
        df = self.get_std_opts()
        mask = df.strategy == "-O0"
        self.baseline = df.loc[mask]
        self.candidate = df.loc[~mask]
        return self._get_speedups()

    
