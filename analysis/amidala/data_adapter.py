import pandas as pd
import hashlib
class DataAdapter:
    def rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        assert type(df) is pd.DataFrame, f'Expecting df to be of type {pd.DataFrame}, but received {type(df)}'
        assert 'name' in list(df.columns), f'Expecting "name" to be in the data frame columns'

        return df.rename(columns={'name':'bench'})

    def add_experiment_id(self, df: pd.DataFrame) -> pd.DataFrame:
        assert type(df) is pd.DataFrame, f'Expecting df to be of type {pd.DataFrame}, but received {type(df)}'
        columns = list(df.columns)
        assert 'experiment_datetime' in columns, 'Columns should have "experiment_datetime"'
        assert 'sequence_requested' in columns, 'Columns should have "sequence_requested"'

        df.loc[:,['experiment_id']] = self._hash_column(df, 'experiment_datetime')
        df.loc[:,['phases_id']] = self._hash_column(df, 'sequence_requested')
        return df

    def add_phases_id(self, df: pd.DataFrame) -> pd.DataFrame:
        assert type(df) is pd.DataFrame, f'Expecting df to be of type {pd.DataFrame}, but received {type(df)}'

        df.loc[:,['phases_id']] = self._hash_column(df, 'sequence_requested')
        return df

    def add_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        columns = self.non_metrics + self.metrics
        assert type(df) is pd.DataFrame, f'Expecting df to be of type {pd.DataFrame}, but received {type(df)}'
        assert (
                len(columns) == len(df.columns) and
                set(columns).issubset(df.columns)),(
                    f'Missing columns {set(columns) - set(df.columns)}')

        df = df[columns]
        tuples = [(x,'') for x in self.non_metrics] + [('metrics',x) for x in self.metrics]
        df.columns = pd.MultiIndex.from_tuples(tuples)
        return df

    def _hash(self, value: any) -> str:
        return hashlib.sha1(str(value).encode()).hexdigest()

    def _hash_column(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        assert type(df) is pd.DataFrame, f'Expecting df to be of type {pd.DataFrame}, but received {type(df)}'
        assert type(column) is str, f'Expecting column to be of type {str}, but received {type(column)}'

        return df.apply(lambda df: self._hash(df[column]), axis=1)

    def __init__(self):
        self.non_metrics = ['experiment_datetime','toolchain','target','dataset_size','benchmark_suite_name','requested_phase_order_lengths','requested_phase_order_cardinalities','strategy','strategy_seed','phase_order_max_length','phase_order_cardinality','sequence_requested','sequence_executed','has_error','error', 'experiment_id']
        self.metrics = ['cpu_cycles','code_size_in_bytes','l1_dcm','l1_icm','l2_dcm','tlb_dm','tlb_im','hw_int','br_msp','tot_ins','ld_ins','sr_ins','br_ins','l1_dca','l2_dca']
