# Strategies for Compiler Phase Ordering Targeting CPUs

## Introduction
Compilers can optimize programs by performing a sequence of transformation
phases. The set of transformations, along with their order, can significantly
impact the performance of the optimized program. Performance is defined here as
execution time, energy consumption, memory consumption, and code size.

Using the precomputed compiler phase orders usually improves performance, but
it is possible to have better results by individually tailoring compiler
sequences, known as phase ordering, to each specific program and target pair. 

However, exploring sequences of phases is a complex and time-consuming task,
and an exhaustive exploration of all viable sequences is not feasible.
Selecting compiler phases alone represents a complex problem to be solved, and
ordering the phases adds further complexity, making it a long-standing problem
in compiler research.

We propose to develop a Design Space Exploration (DSE) strategy to recommend
phase orders that lead to better performance or similar results but with less
exploration time, than possible with state-of-the-art approaches, while using the
LLVM 12.0 compiler infrastructure and solely targeting computing platforms using the
ARMv8 64-bit architecture.

## Packages
There are three packages `strategies`, `optimizer`, and `analysis`. The `strategies` package implements the strategies to choose sequences of phases to be executed against benchmarks. The `optimizer` package applies sequences of phases to a benchmark suite and generates metrics data. The `analysis` package
- `strategies`
- `optimizer`
- `analysis`

1. **Compiler Phase-Ordering Strategies**
The package `strategies` implements strategies that utilize iterative compilation to address
   the compiler phase ordering problem.

2. **Runner**
The package `optimizer` is responsible for executing phase order sequences. It runs these sequences on a target device and collects
   performance data allowing for evaluation and validation of their impact on program optimization.

3. **Results Analysis**
The package `analysis` plots the data collected with the `optimizer` package. It computes statistics about the performance of the phase sequences following their execution on the target device. It provides insights into the effectiveness of different phase orderings on program performance.

## Prerequisites
- Python 3.7
- LLVM 12.0

## License
This project has an MIT license. See [license.txt](license.txt).
