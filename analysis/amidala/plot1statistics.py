from amidala.plot1data import Plot1Data
import pandas as pd


class Plot1Statistics:
    def compute(self, df):
        baseline = df.loc[df.experiment_id != "e1"]
        candidate = df.loc[df.experiment_id == "e1"]
        idmin = (
            baseline.loc[:, ["benchmark", "cpu_cycles"]]
            .groupby("benchmark")
            .idxmin()
            .cpu_cycles
        )
        best = baseline.loc[idmin]
        res = pd.merge(
            candidate, best, on="benchmark", suffixes=["_candidate", "_best"]
        ).loc[:, ["benchmark", "cpu_cycles_candidate", "cpu_cycles_best"]]
        res["speedup"] = res.cpu_cycles_best / res.cpu_cycles_candidate
        res = res.pivot(columns="benchmark", values="speedup")
        data = Plot1Data()
        data.benchmarks = list(res.benchmark)
        data.cpu_cycles_speedup = list(res.speedup)

        return data
