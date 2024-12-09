#!/usr/bin/env python3 -O

from amidala.compare_runner import CompareRunner
from amidala.query_runner import QueryRunner
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('db', type=click.Path(exists=True))
@click.argument('candidate')
@click.argument('baseline')
@click.argument('plot',default='box')
@click.option('--benchmarks', default='')
@click.option('--save', default='')
@click.option('--sharex',is_flag=True)
@click.option('--show',is_flag=True)
def compare(db, candidate, baseline, plot, benchmarks, save, sharex, show):
    runner = CompareRunner()
    runner.db = db
    runner.plotname = plot
    runner.candidate = candidate
    runner.baseline = baseline
    runner.benchmarks = benchmarks
    runner.save_path = save
    runner.sharex = sharex
    runner.show = show
    runner.run()
    
def _list_experiments(df):
    df = df.drop_duplicates(subset='date')
    return df.loc[:, ['date', 'strategy','length','cardinality','strategy_seed']]

@cli.command()
@click.argument('db', type=click.Path(exists=True))
def list(db):
    print('list [todo]')

@cli.command()
@click.argument('db', type=click.Path(exists=True))
@click.argument('candidate')
@click.argument('baseline')
def query(db, candidate, baseline):
    runner = QueryRunner()
    runner.db = db
    runner.candidate = candidate
    runner.baseline = baseline
    runner.run()

def run():
    cli()
