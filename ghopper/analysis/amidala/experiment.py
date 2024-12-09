from __future__ import annotations
from amidala.statistics_plumber import StatisticsPlumber
from amidala.data_adapter import DataAdapter
import pandas as pd

class Experiment:
    def compare_against_best(self, other: list[Experiment]) -> pd.DataFrame:
        return (
                self._stats
                .compare_against_best(self._df, [x.get_df() for x in other])
                .round(2)
                )

    def get_df(self):
        return self._df

    def __init__(self, df):
        self._df = df
        self._adapter = DataAdapter()
        self._stats = StatisticsPlumber()

    def __len__(self):
        return len(self._df)
