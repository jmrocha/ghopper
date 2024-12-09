from amidala.statistics_plumber import StatisticsPlumber
import unittest
import pandas as pd


class TestStatisticsPlumber(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsPlumber()

    @unittest.skip('')
    def test_get_median(self):
        df = pd.DataFrame(
                {
                    'bench': [
                            'a','a', 'b', 'b',
                            'a', 'a', 'b', 'b'
                            ],
                    'phases_id': [
                        'p1','p1', 'p1', 'p1',
                        'p2','p2', 'p2', 'p2',
                        ],
                    'code_size_in_bytes': [
                        10, 10, 20, 20,
                        10, 10, 20, 20,
                        ],
                    'cpu_cycles': [
                        15, 10, 1, 5,
                        15, 10, 1, 5,
                        ],
                    'l1_dcm': [
                        None, None, None, None,
                        None, None, None, None],
                    'dataset size': [
                        'mini', 'mini', 'mini', 'mini',
                        'mini', 'mini', 'mini', 'mini',
                        ],
                }
                )
        tuples = [
                ('metrics','code_size_in_bytes'),
                ('metrics', 'cpu_cycles'),
                ('metrics', 'l1_dcm'),
                ('dataset size', ''),
                ]
        index = ['phases_id', 'bench']
        df = df.set_index(index)
        df.columns = pd.MultiIndex.from_tuples(tuples)
        expected_median = pd.DataFrame(
            {
                'bench':[
                    'a', 'b',
                    'a', 'b',
                    ],
                'phases_id': [
                    'p1', 'p1',
                    'p2', 'p2',
                    ],
                'dataset size': [
                    'mini', 'mini',
                    'mini', 'mini',
                    ],
                'code_size_in_bytes': [
                    10.0, 20.0,
                    10.0, 20.0,
                    ],
                'cpu_cycles': [
                    12.5, 3.0,
                    12.5, 3.0,
                    ],
                'l1_dcm': [
                    None, None, None, None,
                    ],
            })
        expected_median = expected_median.set_index(index)
        tuples = [
                ('dataset size', ''),
                ('metrics','code_size_in_bytes'),
                ('metrics', 'cpu_cycles'),
                ('metrics', 'l1_dcm'),
                ]
        expected_median.columns = pd.MultiIndex.from_tuples(tuples)

        median = self.stats.get_median(df)
        pd.testing.assert_frame_equal(expected_median, median)

    @unittest.skip('')
    def test_concat_gmean(self):
        stats = StatisticsPlumber()
        df = pd.DataFrame({
            'bench': ['a', 'b', 'a', 'b'],
            'phases_id': ['p1', 'p1', 'p2', 'p2'],
            'cpu_cycles': [1, 10, 15, 20],
            'code_size_in_bytes': [1, 15, 50, 45],
            'dataset size': ['mini', 'mini', 'mini', 'mini'],
            })
        tuples = [
                ('metrics','cpu_cycles'),
                ('metrics', 'code_size_in_bytes'),
                ('dataset size', ''),
                ]
        df = df.set_index(['phases_id', 'bench'])
        df.columns = pd.MultiIndex.from_tuples(tuples)
        gmean = stats.concat_gmean(df)
        expected_df = pd.DataFrame({
            'bench': ['_average', 'a', 'b', '_average', 'a', 'b'],
            'phases_id': ['p1', 'p1', 'p1', 'p2', 'p2', 'p2'],
            'dataset size': ['mini', 'mini', 'mini', 'mini', 'mini', 'mini'],
            'code_size_in_bytes': [3.87298, 1, 15,47.43416, 50, 45],
            'cpu_cycles': [3.16227, 1, 10, 17.32050, 15, 20],
            })
        tuples = [
                ('dataset size', ''),
                ('metrics', 'code_size_in_bytes'),
                ('metrics','cpu_cycles'),
                ]
        expected_df = expected_df.set_index(['phases_id', 'bench'])
        expected_df.columns = pd.MultiIndex.from_tuples(tuples)
        pd.testing.assert_frame_equal(expected_df, gmean)

    def test_compare_against_best(self):
        tuples = [
                ('phases_id', ''),
                ('bench', ''),
                ('metrics','cpu_cycles'),
                ('metrics', 'code_size_in_bytes'),
                ('metrics', 'l1_dcm'),
                ]
        a = pd.DataFrame(
                {
                    'phases_id': ['X', 'Y', 'X', 'Y'],
                    'bench': ['a', 'a', 'b', 'b'],
                    'cpu_cycles': [1.0, 2, 10, 20],
                    'code_size_in_bytes': [1.0, 2, 10, 20],
                    'l1_dcm': [float('nan') for _ in range(4)]
                })
        b = pd.DataFrame(
                {
                    'phases_id': ['O0', 'O1', 'O0', 'O1'],
                    'bench': ['a', 'a', 'b', 'b'],
                    'cpu_cycles': [2, 1, 1.5, 2],
                    'code_size_in_bytes': [20.0, 10.0, 5.0, 30.0],
                    'l1_dcm': [float('nan') for _ in range(4)],
                })
        c = pd.DataFrame(
                {
                    'phases_id': ['O0', 'O1', 'O0', 'O1'],
                    'bench': ['a', 'a', 'b', 'b'],
                    'cpu_cycles': [4.0, 4.0, 6.0, 8.0],
                    'code_size_in_bytes': [80.0, 40.0, 20.0, 120.0],
                    'l1_dcm': [float('nan') for _ in range(4)],
                })

        stats = StatisticsPlumber()
        expected_speedups = pd.DataFrame(
            {
                'phases_id': ['X', 'Y', 'X', 'Y'],
                'bench': ['a', 'a', 'b', 'b'],
                'code_size_in_bytes': [1/10, 2/10, 10/5, 20/5],
                'cpu_cycles': [1/1, 2/1, 10/1.5, 20/1.5],
                'l1_dcm': [float('nan') for _ in range(4)],
            })
        expected_speedups = expected_speedups.set_index(['phases_id','bench'])
        a.columns = pd.MultiIndex.from_tuples(tuples)
        b.columns = pd.MultiIndex.from_tuples(tuples)
        c.columns = pd.MultiIndex.from_tuples(tuples)
        index = ['phases_id','bench']
        a = a.set_index(index)
        b = b.set_index(index)
        c = c.set_index(index)
        speedups = stats.compare_against_best(a, [b,c])
        pd.testing.assert_frame_equal(expected_speedups, speedups)
