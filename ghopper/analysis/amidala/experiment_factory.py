from amidala.experiment import Experiment
import pandas as pd
class ExperimentFactory:
    def __init__(self):
        self.df = None
        self.reducer = None
        self.metric = None
        self.experiment_id = None

    def get(self, idx):
        assert self.df is not None, 'self.df was not defined'

        if '-' in idx:
            self.reducer, self.metric, self.experiment_id = idx.split('-')
            return self._get_reduced_experiment()
        else:
            self.experiment_id = idx
            return self._get_experiment()
        
    def _get_reduced_experiment(self):
        assert self.reducer is not None
        assert self.metric is not None
        assert self.experiment_id is not None

        df = self._get_df_by_experiment_id(self.experiment_id)
        experiment = Experiment(df)
        if self.reducer == 'best':
            return self._get_best_of_experiment(experiment)

    def _get_experiment(self):
        assert self.experiment_id is not None

        df = self._get_df_by_experiment_id(self.experiment_id)
        experiment = Experiment(df)
        return experiment

    def _get_df_by_experiment_id(self, id):
        if id == 'std':
            std_df = self.df.loc[self.df.strategy.str.startswith('-O')]
            mask = std_df.strategy == '-O0'
            return std_df.loc[~mask]
        else:
            return self.df.loc[self.df.date_id == id]

    def _get_best_of_experiment(self, experiment):
        if self.metric == 'cpu':
            return experiment.best_by_cpu_cycles()
        elif self.metric == 'size':
            return experiment.best_by_bin_size()
        else:
            raise ValueError(f'Invalid metric "{self.metric}"')
