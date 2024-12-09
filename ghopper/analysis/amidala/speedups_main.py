#!/usr/bin/env python3

import click
from stats import Stats
from plot import Plot


@click.group()
def cli():
    pass


@cli.command()
@click.argument("data_path")
@click.argument("baseline_id")
@click.argument("candidate_id")
def latex(data_path, baseline_id, candidate_id):
    plot = Plot()
    stats = Stats()
    stats.baseline_id = baseline_id[:7]
    stats.candidate_id = candidate_id[:7]
    stats.data_path = data_path
    stats.init()
    speedups_best_std_opt = stats.get_speedups_against_best_standard_opt()
    # speedups = stats.get_speedups()
    std_opts = stats.get_std_opts()
    std_opts_speedups = stats.get_std_opts_speedups()
    # plot.baseline_id = baseline_id
    # plot.speedups = speedups
    plot.speedups_best = speedups_best_std_opt
    plot.std_opts = std_opts
    plot.std_opts_speedups = std_opts_speedups
    # plot.standard_opts_comparison()
    # plot.strategy_v_best_standard()
    plot.histogram_std_opts()
    plot.std_opts_lengths()
    plot.show()
    """
    fig, axs = plt.subplots(2, 1, sharex=True, sharey=True,
            figsize=set_size(345, fraction=0.9, subplots=(2, 1)))
    plot.show_speedups_against_best_standard_opt(axs[0], plot.speedups_best)
    plot.show_speedups_against_strategy(axs[1], plot.speedups)
    """
    # fig.savefig('s1a-v-std.pgf')


@cli.command()
@click.argument("data_path")
@click.argument("baseline_id")
@click.argument("candidate_id")
def query(data_path, baseline_id, candidate_id):
    plot = Plot()
    stats = Stats()
    stats.baseline_id = baseline_id[:7]
    stats.candidate_id = candidate_id[:7]
    stats.data_path = data_path
    stats.init()
    speedups_best_std_opt = stats.get_speedups_against_best_standard_opt()
    speedups = stats.get_speedups()
    std_opts = stats.get_std_opts()
    std_opts_speedups = stats.get_std_opts_speedups()
    plot.baseline_id = baseline_id
    plot.speedups = speedups
    plot.speedups_best = speedups_best_std_opt
    plot.std_opts = std_opts
    plot.std_opts_speedups = std_opts_speedups
    plot.show_speedups()
    plot.show_std_opts()
    import pdb

    pdb.set_trace()


@cli.command()
@click.argument("data_path")
def list(data_path):
    stats = Stats()
    stats.data_path = data_path
    stats.init()
    print(stats.get_ids())


@cli.command()
@click.argument("data_path")
@click.argument("baseline_id")
@click.argument("candidate_id")
def plot(data_path, baseline_id, candidate_id):
    plot = Plot()
    stats = Stats()
    stats.baseline_id = baseline_id[:7]
    stats.candidate_id = candidate_id[:7]
    stats.data_path = data_path
    stats.init()
    speedups_best_std_opt = stats.get_speedups_against_best_standard_opt()
    speedups = stats.get_speedups()
    std_opts = stats.get_std_opts()
    std_opts_speedups = stats.get_std_opts_speedups()
    plot.baseline_id = baseline_id
    plot.speedups = speedups
    plot.speedups_best = speedups_best_std_opt
    plot.std_opts = std_opts
    plot.std_opts_speedups = std_opts_speedups

    plot.show_speedups()
    plot.show_std_opts()
    plot.show()


cli()
