from amidala.statistics import Statistics
import pandas as pd
import itertools
import hashlib
class Data:
    def columns_df(self, df: pd.DataFrame):
        metadata_columns = list(df.iloc[:,:16].columns) + list(df.iloc[:,-3:].columns)
        metrics_columns = df.iloc[:,16:-3].columns
        columns = list(metadata_columns) + list(metrics_columns) 
        metrics_tuples = list(itertools.product(['metrics'],metrics_columns))
        metadata_tuples = list(itertools.product(metadata_columns, ['']))
        tuples = metadata_tuples + metrics_tuples
        df = df.reindex(columns,axis=1)
        df.columns = pd.MultiIndex.from_tuples(tuples)
        return df

    def rename_df(self, df):
        return df.rename(columns={
            'experiment_datetime': 'date',
            'requested_phase_order_lengths': 'length',
            'requested_phase_order_cardinalities': 'cardinality',
            'sequence_requested': 'phases',
            'name': 'bench'
            })


    def get(self, csv_path: str) -> pd.DataFrame:
        df = self.get_data(csv_path)
        df = self.filter_errors(df)
        df = self.rename_df(df)
        df = self.hash(df)
        df = self.columns_df(df)
        df = self.get_samples(df) 
        df = self.get_average(df) 
        return df

    def get_data(self, path):
        return self.pd.read_csv(path,na_values='None',engine='pyarrow')

    def filter_errors(self, df):
        return df.query('has_error == False')

    def get_samples(self, df):
        return self.stats.get_samples(df).reset_index(drop=True)

    def get_average(self, df):
        return self.stats.get_average(df).reset_index(drop=True)

    def hash(self, df):
        df.loc[:, ['phases_id']] = df.apply(lambda x: hashlib.sha1(str(x.phases).encode()).hexdigest(), axis=1)
        df.loc[:, ['sequence_executed_id']] = df.apply(lambda x: hashlib.sha1(str(x.sequence_executed).encode()).hexdigest(), axis=1)
        df.loc[:, ['date_id']] = df.apply(lambda x: hashlib.sha1(str(x.date).encode()).hexdigest(), axis=1)
        return df

    def get_std_opts(self, df):
        return df.loc[df.strategy.str.startswith('-O')]

    def get_best_std(self, df):
        return df[['bench', 'metrics']].sort_index(axis=1).dropna(axis=1).groupby('bench').idxmin().metrics

    def __init__(self):
        self.pd = pd
        self.stats = Statistics()
