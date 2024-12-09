import pandas as pd
from scipy.stats import gmean
import collections

class StatisticsPlumber:
    def get_median(self, df: pd.DataFrame) -> pd.DataFrame:
        self._assert_type_dataframe(df)
        self._assert_type_multiindex(df.columns)
        self._assert_columns_exist(['metrics'],df.columns)
        self._assert_index_is(['phases_id','bench'], df.index)

        median = (
                df[['metrics']]
                .groupby(df.index.names)
                .median()
                )
        left, right = df.align(median,axis=1)
        left = left.loc[~left.index.duplicated()]
        left.update(right)
        return left

    def _assert_type_dataframe(self, df: pd.DataFrame):
        assert type(df) is pd.DataFrame, (
                f"Expecting (df) {pd.DataFrame}, but received {type(df)}.")
    
    def _assert_type_multiindex(self, columns: pd.MultiIndex):
        assert type(columns) is pd.MultiIndex, (
                f"Expecting the given data frame columns to be of type {pd.MultiIndex},"
                f" but received {type(columns)}.")

    def _assert_index_type_multiindex(self, index: pd.MultiIndex):
        assert type(index) is pd.MultiIndex, (
                f"Expecting the given data frame index to be of type {pd.MultiIndex},"
                f" but received {type(index)}.")

    def _assert_columns_exist(self, columns_list: list[str], df_columns: pd.MultiIndex):
        assert set(columns_list).issubset(df_columns.get_level_values(0)),(
                f'Expecting {columns_list} to be level 0 columns'
                f' in the data frame.')

    def _assert_index_is(self, index_list: list[str], index: pd.Index):
        assert (
                len(index_list) == len(index.names) and
                (pd.Index(index_list) == index.names).all()), (
                f'Expecting index to be a {pd.MultiIndex} with names ='
                f' {index_list}. Instead, received'
                f' an index {type(index)} with names = {index.names}.')

    def concat_gmean(self, df: pd.DataFrame) -> pd.DataFrame:
        self._assert_type_dataframe(df)
        self._assert_type_multiindex(df.columns)
        self._assert_columns_exist(['metrics'], df.columns)
        self._assert_index_type_multiindex(df.index)
        self._assert_index_is(['phases_id','bench'], df.index)

        res = []
        for _, group in df.groupby('phases_id'):
            group = group.reset_index().set_index('bench')
            avg = self._concat_gmean(group)
            res.append(avg)
        return pd.concat(res).reset_index().set_index(['phases_id', 'bench'])

    def _concat_gmean(self, df: pd.DataFrame) -> pd.DataFrame:
        self._assert_type_dataframe(df)
        self._assert_type_multiindex(df.columns)
        self._assert_columns_exist(['metrics'], df.columns)
        self._assert_index_is(['bench'], df.index)

        avg = (
            df[['metrics']]
            .agg([gmean])
            .rename(index={"gmean": "_average"})
        )
        avg.index.rename('bench', inplace=True)
        left, right = df.align(avg, method="bfill")
        left.update(right)
        return left

    def compare_against_best(self, a: pd.DataFrame, b: list[pd.DataFrame]) -> pd.DataFrame:
        self._assert_type_dataframe(a)
        assert iter(b)
        self._assert_type_multiindex(a.index)
        self._assert_index_is(['phases_id','bench'], a.index)
        self._assert_type_multiindex(a.columns)
        self._assert_columns_exist(['metrics'], a.columns)

        b = pd.concat(b)
        best = b.stack().groupby(level=[1,2],axis=0).min().unstack()
        df = a.join(best, lsuffix='_a', rsuffix='_b')

        return df.metrics_a / df.metrics_b
