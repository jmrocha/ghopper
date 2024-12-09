#!/usr/bin/env python3

from ervin.strategy import StrategyFactory, InvalidStrategy
from ervin.engine import Engine
from ervin.json_encoder import ResultJsonEncoder
from ervin.graph.graph_importer import GraphImporter
from ervin.graph.json_exporter import JsonExporter
import click
import sys
import json

PHASES_O3 = ['-branch-prob', '-sccp', '-inferattrs', '-annotation-remarks', '-early-cse-memssa', '-tailcallelim', '-assumption-cache-tracker', '-licm', '-cg-profile', '-aa', '-adce', '-postdomtree', '-openmpopt', '-aggressive-instcombine', '-gvn', '-loop-sink', '-phi-values', '-lazy-block-freq', '-memdep', '-globaldce', '-loop-vectorize', '-memoryssa', '-loop-distribute', '-correlated-propagation', '-scalar-evolution', '-memcpyopt', '-verify', '-barrier', '-tti', '-dse', '-loop-unroll', '-float2int', '-early-cse', '-basic-aa', '-globals-aa', '-vector-combine', '-called-value-propagation', '-scoped-noalias-aa', '-loops', '-loop-accesses', '-lazy-branch-prob', '-prune-eh', '-slp-vectorizer', '-loop-unswitch', '-speculative-execution', '-instcombine', '-instsimplify', '-loop-rotate', '-jump-threading', '-callsite-splitting', '-mem2reg', '-constmerge', '-domtree', '-pgo-memop-opt', '-reassociate', '-loop-deletion', '-opt-remark-emitter', '-lower-constant-intrinsics', '-simplifycfg', '-lazy-value-info', '-loop-load-elim', '-loop-idiom', '-ee-instrument', '-inline', '-div-rem-pairs', '-sroa', '-ipsccp', '-profile-summary-info', '-targetlibinfo', '-basiccg', '-lcssa', '-annotation2metadata', '-transform-warning', '-elim-avail-extern', '-demanded-bits', '-argpromotion', '-globalopt', '-rpo-function-attrs', '-lcssa-verification', '-alignment-from-assumptions', '-bdce', '-loop-simplify', '-libcalls-shrinkwrap', '-deadargelim', '-mldst-motion', '-forceattrs', '-block-freq', '-indvars', '-lower-expect', '-tbaa', '-inject-tli-mappings', '-strip-dead-prototypes', '-function-attrs'] 

@click.command()
@click.option('--length')
@click.option('--cardinality')
@click.option('--strategy', default='s0')
@click.option('--seed', type=click.Path())
@click.option('--seed-description')
@click.option('--pretty', is_flag=True)
@click.option('--to-graph', 'to_graph', type=click.Path(exists=True))
def main(length, cardinality, strategy, seed, seed_description, pretty,
        to_graph):
    if to_graph:
        export_graph(to_graph, pretty)
        sys.exit(0)
        
            
    engine = Engine()
    if length:
        engine.length = length
    if cardinality:
        engine.cardinality = cardinality
    if seed_description:
        engine.seed = seed_description
    
    factory = StrategyFactory()
    if seed:
        with open(seed, 'r') as f:
            factory.seed = f.read()
    try:
        strategy = factory.get_strategy(strategy)
    except KeyError:
        strategies = factory.get_available_strategies()
        print('Strategy does not exist.'
                f' Try {strategies}'
                    )
        sys.exit(1)
    
    if strategy.phases == []:
        strategy.phases = PHASES_O3
        engine.seed = 'o3'
    engine.strategy = strategy
    result = engine.run()
    result_encoded = encode(result, pretty)
    print(result_encoded)

def encode(result, pretty):
    indent = None 
    if pretty:
        indent = 2
    return ResultJsonEncoder(indent=indent).encode(result)

def export_graph(to_graph, pretty):
    sequences = ''
    with open(to_graph, 'r') as f:
        sequences = f.read()
    importer = GraphImporter()
    graph = importer.from_string(sequences)
    exporter = JsonExporter()
    encoded = exporter.to_json(graph)
    indent=None
    if pretty:
        indent=2
    print(json.dumps(encoded, indent=indent))


main()
