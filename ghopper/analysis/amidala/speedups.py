import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gmean


def get_speedups(candidate, baseline):
    speedups = (
        candidate.set_index("benchmark")
        .loc[:, ["measurement_id", "cpu_cycles"]]
        .join(
            baseline.set_index("benchmark").loc[:, ["measurement_id", "cpu_cycles"]],
            rsuffix="_baseline",
        )
    )
    speedups["speedup"] = speedups.cpu_cycles_baseline / speedups.cpu_cycles
    speedups = speedups.reset_index().set_index("measurement_id")
    del speedups["cpu_cycles"]
    del speedups["cpu_cycles_baseline"]
    del speedups["benchmark"]
    return candidate.set_index("measurement_id").merge(
        speedups, left_index=True, right_index=True
    )


def _get_pivot(df):
    return df.pivot(index="phases_requested_id", columns="benchmark", values="speedup")


def show_speedups(ax, speedups):
    speedups = _get_pivot(speedups)
    ax.boxplot(speedups.values, labels=speedups.columns.values)
    ax.tick_params(axis="x", rotation=45)


def filter_median(df):
    df_median = df.groupby("measurement_id").median()
    df_uniq = df.drop_duplicates(subset="measurement_id").set_index("measurement_id")
    df_uniq.update(df_median)
    return df_uniq.reset_index()


def get_best(df):
    return df.groupby("benchmark", as_index=False).min()


def get_experiment(df, id):
    return df.query(f'experiment_id == "{id}"')


def concat_gmean(df):
    df_gmean = df.loc[:, ["suite_id", "cpu_cycles"]].groupby("suite_id").agg(gmean)
    df_metadata = df.drop_duplicates(subset="suite_id").set_index("suite_id")
    df = df.set_index("suite_id")
    del df_metadata["cpu_cycles"]
    del df_metadata["measurement_id"]
    df_gmean = df_gmean.join(df_metadata)
    df_gmean.loc[:, "benchmark"] = "!ALL"
    # todo: replace measurement_id with hash(suite_id, benchmark)
    df_gmean.loc[:, "measurement_id"] = df_gmean.apply(
        lambda x: hash((x.benchmark, x.strategy, x.phases_requested_id)), axis=1
    )
    df = pd.concat([df, df_gmean])
    return df.reset_index()
