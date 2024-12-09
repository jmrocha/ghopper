from amidala.data_adapter import DataAdapter
from unittest import TestCase
import pandas as pd

class TestDataAdapter(TestCase):
    def setUp(self):
        self.adapter = DataAdapter()
        self.adapter.non_metrics = [
                'experiment_datetime',
                'bench',
                'phases_id'
                ]
        self.adapter.metrics = ['cpu_cycles','code_size_in_bytes']
        self.df = pd.DataFrame({
            'experiment_datetime': ['2022-07-13 12:47:57.481668'],
            'sequence_requested': ['-a -b'],
            'name': ['a']
            })

    def test_rename_columns(self):
        df_adapted = self.adapter.rename_columns(self.df)
        expected_columns = [
                'experiment_datetime',
                'sequence_requested',
                'bench']
        columns = list(df_adapted.columns)
        self.assertEqual(expected_columns, columns)

    def test_add_experiment_id(self):
        df = self.adapter.add_experiment_id(self.df)
        self.assertEqual(df.experiment_id.values[0], 'a16be8401bb6cfdae0a5049327439b5c7bf41935')

    def test_add_phases_id(self):
        df = self.adapter.add_phases_id(self.df)
        self.assertEqual(df.phases_id.values[0], '4c2858c4d4897bdb32a83e4db2b9b62640cce778')

    def test_add_metrics(self):
        self.adapter.non_metrics = []
        df = pd.DataFrame(
                {
                    'bench': [1],
                    'phases_id': [1],
                    'cpu_cycles': [1],
                    'code_size_in_bytes': [1]
                })
        df = df.set_index(['phases_id','bench'])
        df = self.adapter.add_metrics(df)

        self.assertEqual(pd.MultiIndex, type(df.columns))
        self.assertTrue('metrics' in df.columns.get_level_values(0))
