# Performance Benchmarks

This document provides information about the performance benchmarks for the Morse Code Converter project.

## Overview

The benchmarks measure the performance of key operations in the Morse Code Converter:

1. **Text-to-Morse conversion**: Measures how long it takes to convert text to Morse code for different text lengths.
2. **Morse-to-text conversion**: Measures how long it takes to convert Morse code to text for different text lengths.
3. **Sine wave generation**: Measures how long it takes to generate sine waves for different durations.

## Running the Benchmarks

To run the benchmarks, use the `benchmark.py` script:

```bash
python benchmark.py
```

By default, the script runs each benchmark 100 times for each input size and reports statistics about the execution
times.

### Command-line Options

You can customize the benchmarks using the following command-line options:

- `--iterations N`: Run each benchmark N times (default: 100)
- `--text-lengths L1 L2 ...`: Specify the text lengths to benchmark (default: 10, 50, 100, 500, 1000)
- `--durations D1 D2 ...`: Specify the durations (in seconds) to benchmark for sine wave generation (default: 0.01,
  0.05, 0.1, 0.5, 1.0)

Example:

```bash
python benchmark.py --iterations 50 --text-lengths 20 100 1000 --durations 0.1 0.5 1.0
```

## Interpreting the Results

The benchmark results are presented in tables with the following columns:

- **Input Size**: The size of the input (text length or duration)
- **Min (s)**: The minimum execution time in seconds
- **Max (s)**: The maximum execution time in seconds
- **Mean (s)**: The mean (average) execution time in seconds
- **Median (s)**: The median execution time in seconds
- **StdDev (s)**: The standard deviation of the execution times in seconds

Example output:

```
Text to Morse Code Conversion
--------------------------------------------------------------------------------
Input Size Min (s)    Max (s)    Mean (s)   Median (s) StdDev (s)
--------------------------------------------------------------------------------
10         0.000012   0.000089   0.000015   0.000014   0.000008
50         0.000057   0.000132   0.000063   0.000061   0.000009
100        0.000112   0.000187   0.000121   0.000119   0.000011
500        0.000559   0.000712   0.000583   0.000578   0.000023
1000       0.001119   0.001312   0.001156   0.001148   0.000034
```

### Analyzing the Results

When analyzing the benchmark results, consider the following:

1. **Execution time growth**: How does the execution time grow as the input size increases? Is it linear, quadratic, or
   something else?
2. **Variability**: How much do the execution times vary? A high standard deviation indicates inconsistent performance.
3. **Outliers**: Are there any outliers (very high or very low execution times)? These might indicate issues with the
   benchmarking environment or the code.

## Adding New Benchmarks

To add a new benchmark:

1. Create a new function in `benchmark.py` that measures the performance of the operation you want to benchmark.
2. Add the new benchmark to the `main()` function.
3. Update this documentation to include information about the new benchmark.

## Performance Optimization

If the benchmarks reveal performance issues, consider the following optimization strategies:

1. **Algorithm improvements**: Can you use a more efficient algorithm?
2. **Data structure changes**: Are you using the most appropriate data structures?
3. **Caching**: Can you cache results to avoid redundant computations?
4. **Profiling**: Use a profiler to identify specific bottlenecks in the code.

## Benchmark Environment

When reporting benchmark results, it's important to include information about the environment in which the benchmarks
were run:

- Hardware specifications (CPU, RAM)
- Operating system
- Python version
- Any relevant system load or background processes

This information helps others interpret and reproduce the benchmark results.