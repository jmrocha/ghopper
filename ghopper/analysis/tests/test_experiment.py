from amidala.experiment import Experiment
import unittest
import pandas as pd

class TestExperiment(unittest.TestCase):
    @unittest.skip('')
    def test_compare_against_best(self):
        a = pd.DataFrame(
                {
                    'bench': 
                        [
                            'a', 'a',
                            'b', 'b',],
                    'phases_id': 
                        [
                            'X', 'Y',
                            'X', 'Y',
                            ],
                    'cpu_cycles': 
                        [
                            1, 2, 
                            10, 20,
                            ],
                    'code_size_in_bytes': 
                        [
                            1, 2,
                            10, 20,
                            ],
                    'dataset size': ['mini','mini','mini','mini'],
                    'strategy': ['s1','s1','s2','s2']
                })
        b = pd.DataFrame(
                {
                    'bench': [
                        'a', 'a',
                        'b', 'b'],
                    'phases_id': [
                        'O0', 'O1',
                        'O0', 'O1'],
                    'cpu_cycles': [
                        2, 1,
                        1.5, 2, ],
                    'code_size_in_bytes': 
                        [
                            20, 10,
                            5, 30],
                    'dataset size': ['mini','mini','mini','mini'],
                    'strategy': ['s1','s1','s2','s2']
                })
        index = ['phases_id','bench']
        columns = pd.MultiIndex.from_tuples(
                [
                    ('metrics','cpu_cycles'),
                    ('metrics','code_size_in_bytes'),
                    ('dataset size',''),
                    ('strategy',''),
                    ])
        a = a.set_index(index)
        b = b.set_index(index)
        a.columns = columns
        b.columns = columns
        e1 = Experiment(a)
        e2 = Experiment(b)
        speedups = e1.compare_against_best(e2)

        self.assertEqual(4, len(speedups))
        self.assertTrue('strategy' in speedups)

    @unittest.skip('')
    def test_get_best(self):
        df = pd.DataFrame(
                {
                    'phases_id': ['x', 'y'],
                    'bench': ['a', 'a'],
                    'cpu_cycles': [1, 2],
                    'strategy': ['s1','s2']
                })

        index = ['phases_id','bench']
        df = df.set_index(index)
        best = df[['cpu_cycles']].groupby(level=[1],axis=0).idxmin()

        print()
        print(df)
        print(best)
        breakpoint()

    @unittest.skip('')
    def test_best(self):
        df = pd.DataFrame(
                {
                    'phases_id': [
                        'x', 'y',
                        'x','y'],
                    'bench': [
                        'a', 'a',
                        'b', 'b'],
                    'cpu_cycles': [
                        1, 100,
                        100, 2],
                    'size': [
                        100,3,
                        4,100],
                    'strategy': [
                        's1','s2',
                        's1','s2']
                })
        df = df.set_index(['phases_id','bench'])
        min = df[['cpu_cycles','size']].groupby('bench').min()
        idxmin = df[['cpu_cycles','size']].groupby('bench').idxmin()
        breakpoint()

    @unittest.skip('')
    def test_unstack(self):
        index = pd.MultiIndex.from_product([['x','y'],['a','b'], ['s1']],
                names=['phases_id','bench', 'strategy'])
        columns = ['cpu','size']
        data = [
                [1,10],
                [10,1],
                [10,1],
                [1,10],
                ]
        df = pd.DataFrame(data,index=index,columns=columns)
        res = self._get_res()
        breakpoint()

    @unittest.skip('')
    def test_unstack_2(self):
        data = [
                [1.1,1.3],
                ['o2','o3'],
                [1.1,1.7],
                ['os','o1'],
                [1.1,1.3],
                ['o0','os'],
                [1.1,1.7],
                ['o2','o2'],
                ] 
        index = pd.MultiIndex.from_product(
                [['x','y'],['a','b'], ['speedup','strategy']],
                names=['phases_id','bench', ''])
        df = pd.DataFrame(data, index=index, columns=['cpu','size'])
        

    def _get_res(self):
        index = pd.MultiIndex.from_product([['x','y'],['a','b']],
                names=['phases_id','bench'])
        columns = pd.MultiIndex.from_product(
                [['cpu','size'],['best_value','best_strategy']],
                names=['metric', 'field'])
        data = [
                [1.1, 'O3', 1.2, 'Os'],
                [0.5, 'O2', 1.1, 'O1'],
                [3.1, 'Os', 1.8, 'Os'],
                [2.1, 'O3', 1.9, 'O2'],
                ]
        return pd.DataFrame(data, index=index,columns=columns)

    @unittest.skip('')
    def test_join(self):
        index = pd.Index(['a','b'],name='bench')
        data = [1,2]
        data = [[1,2],[3,4]]
        columns = pd.MultiIndex.from_product([['cpu'],['speedup']])
        columns = pd.MultiIndex.from_product([['cpu','size'],['speedup']])
        df = pd.DataFrame(data, index=index,columns=columns)
        columns = pd.MultiIndex.from_product([['cpu','size'],['strategy']])
        data = ['o1','o2']
        data = [['o1','o2'],['o1','o2']]
        df2 = pd.DataFrame(
                data,
                index=index,
                columns=columns)
