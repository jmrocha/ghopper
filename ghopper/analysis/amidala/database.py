from amidala.experiment import Experiment
from amidala.data_adapter import DataAdapter
from amidala.statistics_plumber import StatisticsPlumber
import pandas as pd
class Database:
    def read(self) -> None:
        df = self.pd.read_csv(self.path, na_values="None",
                dtype={'hw_int': str,
                    'requested_phase_order_lengths': str,
                    'requested_phase_order_cardinalities': str,
                    'strategy_seed': str,
                    'error': str,
                    'hw_int': float
                    })
        df = self.adapter.add_experiment_id(df)
        self.df = df

    def get_experiment_by_id(self, id: str) -> Experiment:
        assert self.df is not None, 'The data frame df was not defined'
        assert type(id) is str, f'Expecting id to be of type {str}'
        assert 'experiment_id' in self.df, 'The experiment_id was not added'

        df = self.df.query(f'experiment_id == "{id}"')
        df = self.adapter.rename_columns(df)
        df = self.adapter.add_phases_id(df)
        df = df.set_index(['phases_id','bench'])
        df2 = self.adapter.add_metrics(df)
        df2 = self.stats.get_median(df2)
        df2 = self.stats.concat_gmean(df2)
        return Experiment(df2)

    def set_df(self, df: pd.DataFrame) -> None:
        self.df = df

    def __init__(self, path: str) -> None:
        assert type(path) is str, (
                f'Expecting path to be of type {str},'
                f'but received {type(path)}')
        self.path = path
        self.df = None
        self.adapter = DataAdapter()
        self.stats = StatisticsPlumber()
        self.pd = pd
