from ghopper.experiment_observation import ExperimentObservation


class ExperimentRunner:
    def __init__(self):
        self.experiment_observation = ExperimentObservation()

    def experiment_observed(self, obs):
        self.experiment_observation = obs
