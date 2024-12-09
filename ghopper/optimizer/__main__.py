#!/usr/bin/env python3


from ghopper.app import App
import click
import yaml

def configure(ctx, param, filename):
    if filename is None:
        return
    
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
    ctx.default_map = {
            'benchmark_suite_path': data['config']['benchmark_suite_path'],
            'phase_orders_path': data['config']['phase_orders_path'],
            'benchmark_timeout_in_s': data['config']['benchmark_timeout_in_s'],
            'output_path': data['config']['output_path'],
            'benchmark_suite_name': data['metadata']['benchmark_suite_name'],
            'target': data['metadata']['target'],
            'toolchain': data['metadata']['toolchain'],
            'dataset_size': data['metadata']['dataset_size'],
            }

@click.command()
@click.argument('benchmark_suite_path', type=click.Path(exists=True))
@click.argument('phase_orders_path', type=click.Path(exists=True))
@click.option("--timeout", 'benchmark_timeout_in_s', type=float, default=300)
@click.option("--sample-size", 'sample_size', type=int, default=1)
@click.option("--suite-name", 'benchmark_suite_name', type=str, default='')
@click.option("--target", type=str, default='')
@click.option("--toolchain", type=str, default='')
@click.option("--dataset-size", 'dataset_size', type=str, default='')
@click.option("--output", 'output_path', type=str, default='out.csv')
@click.option("--config", callback=configure, type=click.Path(exists=True))
def main(benchmark_suite_path, phase_orders_path, benchmark_timeout_in_s, sample_size,
        benchmark_suite_name, target, toolchain, dataset_size, output_path, config):
    app = App()
    app.benchmark_suite_path = benchmark_suite_path
    app.phase_orders_path = phase_orders_path
    app.timeout_in_s = benchmark_timeout_in_s
    app.sample_size = sample_size
    app.output_path = output_path
    app.experiment_metadata.toolchain = toolchain
    app.experiment_metadata.target = target
    app.experiment_metadata.dataset_size = dataset_size
    app.experiment_metadata.benchmark_suite_name = benchmark_suite_name
    app.run()

main()
