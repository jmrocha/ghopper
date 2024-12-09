import pandas as pd
from scipy.stats import gmean

date = "date_id"
strategy = "strategy"
length = "length"
cardinality = "cardinality"
phases = "phases_id"
bench = "bench"
metrics = "metrics"
samples_group = [date, strategy, length, cardinality, phases, bench]
samples_fields = samples_group + [metrics]
average_fields = [bench, metrics]
average_group = [date, strategy, length, cardinality, phases]


class Statistics:
    def get_samples(self, df: pd.DataFrame) -> pd.DataFrame:
        assert (
            type(df) is pd.DataFrame
        ), f"Expecting {pd.DataFrame}, but received {type(df)}"
        assert (
            type(df.columns) is pd.MultiIndex
        ), f"Expecting columns to be of type {pd.MultiIndex}, but received {type(df.columns)}"
        assert set(samples_fields).issubset(
            df.columns.get_level_values(0)
        ), f"{samples_fields} need to be in the columns of the given DataFrame"

        median = (
            df[samples_fields]
            .sort_index(axis=1)
            .groupby(samples_group)
            .median()
        )
        df = df.set_index(samples_group)
        left, right = df.align(median,axis=1)
        left.update(right)
        return left.drop_duplicates().reset_index()

    def get_average(self, df: pd.DataFrame) -> pd.DataFrame:
        assert (
            type(df) is pd.DataFrame
        ), f"Expecting {pd.DataFrame}, but received {type(df)}"
        assert (
            type(df.columns) is pd.MultiIndex
        ), f"Expecting columns to be of type {pd.MultiIndex}, but received {type(df.columns)}"
        assert set(average_group).issubset(
            df.columns.get_level_values(0)
        ), f"{average_group} need to be in the columns of the given DataFrame, but received {df.columns.values}"

        res = []
        for _, group in df.groupby(average_group):
            avg = self._get_benchmark_suite_average(group)
            res.append(avg)
        return pd.concat(res)

    def _get_benchmark_suite_average(self, df: pd.DataFrame) -> pd.DataFrame:
        assert (
            type(df) is pd.DataFrame
        ), f"Expecting {pd.DataFrame}, but received {type(df)}"
        assert (
            type(df.columns) is pd.MultiIndex
        ), f"Expecting columns to be of type {pd.MultiIndex}, but received {type(df.columns)}"
        assert set(average_fields).issubset(
            df.columns.get_level_values(0)
        ), f"{average_fields} need to be columns in the given DataFrame"
        assert len(df.bench) == len(
            set(df.bench)
        ), f"Expecting one benchmark suite, which has unique benchmarks, but received duplicated ones: {df.bench.values}"

        avg = (
            df.set_index(bench)[[metrics]]
            .dropna(axis=1)
            .agg([gmean])
            .rename(index={"gmean": "_average"})
        )
        avg.index.rename(bench, inplace=True)
        left, right = df.set_index(bench).align(avg, method="bfill")
        left.update(right)
        return left.reset_index()

    def get_speedups(
        self, candidate: pd.DataFrame, baseline: pd.DataFrame
    ) -> pd.DataFrame:
        speedups_fields = [bench, phases, metrics]
        assert (
            type(candidate) is pd.DataFrame
        ), f"Expecting (candidate) {pd.DataFrame}, but received {type(df)}"
        assert (
            type(baseline) is pd.DataFrame
        ), f"Expecting (baseline) {pd.DataFrame}, but received {type(df)}"
        assert (
            type(candidate.columns) is pd.MultiIndex
        ), f"Expecting (candidate) columns to be of type {pd.MultiIndex}, but received {type(df.columns)}"
        assert (
            type(baseline.columns) is pd.MultiIndex
        ), f"Expecting (baseline) columns to be of type {pd.MultiIndex}, but received {type(df.columns)}"
        assert set(speedups_fields).issubset(
            candidate.columns.get_level_values(0)
        ), f"{speedups_fields} need to be columns in the given DataFrame (candidate)"
        assert set(speedups_fields).issubset(
            baseline.columns.get_level_values(0)
        ), f"{speedups_fields} need to be columns in the given DataFrame (baseline)"

        candidate = candidate.set_index([bench, phases])[[metrics]]
        baseline = baseline.set_index([bench])[[metrics]]
        speedups = candidate.join(
            baseline, lsuffix="_candidate", rsuffix="_baseline", on=bench
        )
        speedups = speedups.metrics_baseline / speedups.metrics_candidate
        speedups.columns = pd.MultiIndex.from_product(
            [["metrics_speedups"], speedups.columns]
        )
        return speedups

    def compare(self, candidate, baseline):
        speedups = self.get_speedups(candidate, baseline)
        speedups = speedups['metrics_speedups'].reset_index().pivot(columns=bench,index=phases,values=speedups.columns.get_level_values(1))
        return speedups.dropna(axis=1)

    def compare_without_pivot(self, candidate, baseline):
        speedups = self.get_speedups(candidate, baseline)
        #speedups = speedups['metrics_speedups'].reset_index().pivot(columns=bench,index=phases,values=speedups.columns.get_level_values(1))
        return speedups.dropna(axis=1)
