import unittest
import pandas as pd

class TestAmidala(unittest.TestCase):
    @unittest.skip('')
    def test_hello(self):
        data = [
                ['a','x',1,2, 'o1'],
                ['a','y',3,4, 'o2'],
                ['b','x',5,6,'o1'],
                ['b','y',7,8,'o2'],
                ]
        columns = ['bench','phases_id','cpu','size','strategy']
        df = pd.DataFrame(data, columns=columns)
        df = df.melt(id_vars=['bench','phases_id','strategy'])
        df = df.groupby(['bench','variable']).min().stack().swaplevel().unstack().unstack()
        """df_min = df[['cpu','size']].stack().groupby(level=[0,2]).idxmin()
        df_join = df.stack()[df_min]
        y = x.to_frame().join(df,on=['phases_id','bench']).unstack()
        print(f'\n{df}')
        print(f'{df_min}')
        """

    def test_melt(self):
        data = [
                ['x','o1',1],
                ['x','o1',2],
                ['y','o2',3],
                ['y','o2',4],
                ]
        data2 = [
                ['x','o1',5],
                ['x','o1',6],
                ['y','o2',7],
                ['y','o2',8],
                ]
        index = pd.MultiIndex.from_product([['a','b'],['cpu','size']], names=[
            'bench','metric'])
        columns = ['phases_id', 'strategy', 'value']
        df = pd.DataFrame(data, index, columns)
        df2 = pd.DataFrame(data2, index, columns)
