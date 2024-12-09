import matplotlib.pyplot as plt

PGF_BASE_PATH = "/Users/jrocha/thesis/monography/src/assets/pgf"
colors = {"-O0": "green", "-O1": "red", "-O2": "orange", "-O3": "blue", "-Os": "brown"}


def set_size(width_pt, fraction=1, subplots=(1, 1)):
    """Set figure dimensions to sit nicely in our document.

    Parameters
    ----------
    width_pt: float
            Document width in points
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy
    subplots: array-like, optional
            The number of rows and columns of subplots.
    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure (in pts)
    fig_width_pt = width_pt * fraction
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    golden_ratio = (5 ** 0.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

    return (fig_width_in, fig_height_in)


class Plot:
    def __init__(self):
        self.speedups = None
        self.speedups_best = None
        self.baseline_id = None
        self.std_opts = None
        self.std_opts_speedups = None

    def standard_opts_comparison(self):
        fig, ax = plt.subplots(figsize=set_size(426.79135, fraction=1))
        self.show_std_speedups(ax, self.std_opts_speedups)
        fig.savefig("std-opts-speedup.pgf", bbox_inches="tight")

    def strategy_v_best_standard(self):
        fig, ax = plt.subplots(figsize=set_size(426.79135, fraction=1))
        ax.axhline(y=1, ls="--", color="green")
        speedups = self._get_pivot(self.speedups_best).dropna()
        speedups.plot(kind="box", ax=ax)
        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation=45,
            rotation_mode="anchor",
            ha="right",
            fontsize=8,
        )
        ax.set_title("CPU Cycles Speedup v. Best -O")
        ax.set_xlabel("Benchmark")
        ax.set_ylabel("CPU Cycles Speedup")
        fig.savefig("strategy-v-standard-opts.pgf", bbox_inches="tight")

    def show_speedups_against_best_standard_opt(self, ax, speedups):
        self._show_speedups(ax, speedups)
        ax.set_title("CPU cycles speedups against the best -O")
        ax.set_ylabel("speedup")

    def show_speedups_against_strategy(self, ax, speedups):
        self._show_speedups(ax, speedups)
        ax.set_title(f"CPU cycles speedups against {self.baseline_id}")
        ax.set_ylabel("speedup")
        ax.set_xlabel("benchmark")

    def show_speedups(self):
        fig, axs = plt.subplots(2, 1, sharex=True, sharey=True)
        self.show_speedups_against_best_standard_opt(axs[0], self.speedups_best)
        self.show_speedups_against_strategy(axs[1], self.speedups)

    def show_std_opts(self):
        fig, axs = plt.subplots(2, 1)
        self.show_cpu_cycles(axs[0], self.std_opts)
        self.show_std_speedups(axs[1], self.std_opts_speedups)

    def show_cpu_cycles(self, ax, df):
        df = df.pivot(index="benchmark", columns="strategy", values="cpu_cycles")
        df.plot(
            kind="bar",
            ax=ax,
            sharex=True,
            sort_columns=True,
            rot=45,
            color=df.columns.map(colors),
        )
        ax.set_title("CPU cycles (only standard optimizations)")
        ax.set_ylabel("CPU cycles")
        ax.legend(title="Strategy")

    def show_std_speedups(self, ax, speedups):
        ax.axhline(y=1, ls="--", color="green")
        df = speedups.pivot(index="benchmark", columns="strategy", values="speedup")
        df.plot(
            kind="bar",
            ax=ax,
            sharex=True,
            sort_columns=True,
            rot=45,
            fontsize=8,
            color=df.columns.map(colors),
        )
        ax.set_xticklabels(
            ax.get_xticklabels(), rotation=45, rotation_mode="anchor", ha="right"
        )
        ax.set_title("CPU cycles speedup against -O0 (only standard optimizations)")
        ax.set_ylabel("CPU cycles speedup")
        ax.legend(title="Strategy")

    def _show_speedups(self, ax, speedups):
        ax.axhline(y=1, ls="--", color="green")
        speedups = self._get_pivot(speedups).dropna()
        ax.boxplot(speedups.values, labels=speedups.columns.values)
        ax.tick_params(axis="x", rotation=45)

    def _get_pivot(self, df):
        return df.pivot(
            index="phases_requested_id", columns="benchmark", values="speedup"
        )

    def show(self):
        plt.show()

    def histogram_std_opts(self):
        fig, ax = plt.subplots()
        max = self.std_opts_speedups.groupby("benchmark").speedup.idxmax()
        df = self.std_opts_speedups.loc[max].loc[
            :, ["strategy", "benchmark", "speedup"]
        ]
        df = df["strategy"].value_counts()
        rects = ax.bar(df.index, df.values)
        ax.bar_label(rects)
        ax.set_xlabel("Strategy")
        ax.set_ylabel("Number of Speedups")
        ax.set_title("Number of Speedups per Standard Optimization Against -O0")
        print(df)
        fig.savefig(f"{PGF_BASE_PATH}/hist-std-opts-speedups.pgf", bbox_inches="tight")
        # x['strategy'].hist()

    def std_opts_lengths(self):
        df = self.std_opts.drop_duplicates("strategy")
        df = df.loc[:, ["phases_executed", "strategy"]]
        df["length"] = df.apply(lambda x: len(x.phases_executed.split()), axis=1)

        # print(df)
        fig, ax = plt.subplots()
        rects = ax.bar(df.strategy, df.length)
        ax.bar_label(rects)
        ax.set_xlabel("Strategy")
        ax.set_ylabel("Number of Phases")
        ax.set_title("Number of Phases per -O")
        fig.savefig(f"{PGF_BASE_PATH}/hist-std-opts-lengths.pgf", bbox_inches="tight")

        return df
