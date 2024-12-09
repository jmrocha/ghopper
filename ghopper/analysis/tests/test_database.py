from amidala.database import Database
from amidala.data_adapter import DataAdapter
from unittest import TestCase
import pandas as pd
import unittest

class TestDatabase(TestCase):
    def setUp(self):
        self._log = []
        self._db = Database('example.csv')
        self._mock_adapter = MockDataAdapter()
        self._mock_pandas = MockPandas()
        self._mock_adapter.log = self._log
        self._mock_pandas.log = self._log
        self._db.pd = self._mock_pandas
        self._db.adapter = self._mock_adapter
        self._df = self._get_df()
        self._mock_adapter.non_metrics = [
                'experiment_datetime',
                'sequence_requested',
                'experiment_id']
        self._mock_adapter.metrics = [
                'cpu_cycles',
                'code_size_in_bytes']

    def _get_df(self):
        return pd.DataFrame({
            'experiment_datetime': [
                '2022-07-13 12:47:57.481668', 
                '2022-07-13 12:47:57.481668',
                ],
            'sequence_requested': [
                '-a -b',
                '-a -b'
                ],
            'name': [
                'a',
                'a'
                ],
            'experiment_id': [
                'e1',
                'e1'
                ],
            'cpu_cycles': [
                3,
                7 
                ],
            'code_size_in_bytes': [
                1,
                4
                ]
            })

    
    @unittest.skip('')
    def test_get_experiment_by_id(self):
        self._db.df = self._df
        e = self._db.get_experiment_by_id('e1')
        index = e.get_df().index.names

        self.assertEqual(2, len(e))
        self.assertEqual(['phases_id','bench'], index)
        self.assertTrue('metrics' in e.get_df())
        self.assertTrue('experiment_datetime' in e.get_df())

    def _get_log(self):
        return ' '.join(self._log)

class MockDataAdapter(DataAdapter):
    def __init__(self):
        super().__init__()
        self.log = []

    def rename_columns(self, df):
        self.log += ['rename_columns']
        return super().rename_columns(df)

    def add_experiment_id(self, df):
        self.log += ['add_experiment_id']
        return super().add_experiment_id(df)

    def add_phases_id(self, df):
        self.log += ['add_phases_id']
        return super().add_phases_id(df)

    def get_log(self):
        return ' '.join(self.log)

class MockPandas:
    def __init__(self):
        self.log = []
        self._read_csv = None

    def return_read_csv(self, value: pd.DataFrame) -> None:
        self._read_csv = value

    def read_csv(self, path, **kwargs):
        args = [path]
        args += [f'{k}={v}' for k, v in kwargs.items()]
        args = ', '.join(args)
        self.log += [f'read_csv({args})']
        return self._read_csv

    def get_log(self):
        return ' '.join(self.log)
