"""
Performance benchmarks for the Morse Code Converter.

This module provides benchmarks for measuring the performance of key operations
in the Morse Code Converter, such as text-to-morse conversion, morse-to-text
conversion, and audio generation.
"""

import argparse
import random
import statistics
import string
import time
from typing import List, Dict, Any, Callable, Tuple

from morse_code import (
    MorseCodeConverterFactory,
    MorseCodePlayer
)


def generate_random_text(length: int) -> str:
    """
    Generate a random text string of the specified length.
    
    Args:
        length (int): The length of the text to generate.
        
    Returns:
        str: A random text string.
    """
    # Include letters, numbers, and some special characters
    chars = string.ascii_uppercase + string.digits + "!?."
    return ''.join(random.choice(chars) for _ in range(length))


def benchmark_function(func: Callable, *args, **kwargs) -> Tuple[float, Any]:
    """
    Benchmark a function by measuring its execution time.
    
    Args:
        func (Callable): The function to benchmark.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
        
    Returns:
        Tuple[float, Any]: A tuple containing the execution time in seconds and the function's return value.
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time, result


def run_benchmark(func: Callable, iterations: int, *args, **kwargs) -> Dict[str, Any]:
    """
    Run a benchmark multiple times and collect statistics.
    
    Args:
        func (Callable): The function to benchmark.
        iterations (int): The number of iterations to run.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
        
    Returns:
        Dict[str, Any]: A dictionary containing benchmark statistics.
    """
    execution_times = []

    for _ in range(iterations):
        execution_time, _ = benchmark_function(func, *args, **kwargs)
        execution_times.append(execution_time)

    return {
        "min": min(execution_times),
        "max": max(execution_times),
        "mean": statistics.mean(execution_times),
        "median": statistics.median(execution_times),
        "stdev": statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
        "iterations": iterations
    }


def benchmark_text_to_morse(text_lengths: List[int], iterations: int = 100) -> Dict[int, Dict[str, Any]]:
    """
    Benchmark text-to-morse conversion for different text lengths.
    
    Args:
        text_lengths (List[int]): A list of text lengths to benchmark.
        iterations (int, optional): The number of iterations for each text length. Defaults to 100.
        
    Returns:
        Dict[int, Dict[str, Any]]: A dictionary mapping text lengths to benchmark statistics.
    """
    converter = MorseCodeConverterFactory.create_converter('international')
    results = {}

    for length in text_lengths:
        text = generate_random_text(length)
        results[length] = run_benchmark(converter.to_morse_code, iterations, text)

    return results


def benchmark_morse_to_text(text_lengths: List[int], iterations: int = 100) -> Dict[int, Dict[str, Any]]:
    """
    Benchmark morse-to-text conversion for different text lengths.
    
    Args:
        text_lengths (List[int]): A list of text lengths to benchmark.
        iterations (int, optional): The number of iterations for each text length. Defaults to 100.
        
    Returns:
        Dict[int, Dict[str, Any]]: A dictionary mapping text lengths to benchmark statistics.
    """
    converter = MorseCodeConverterFactory.create_converter('international')
    results = {}

    for length in text_lengths:
        text = generate_random_text(length)
        morse = converter.to_morse_code(text)
        results[length] = run_benchmark(converter.from_morse_code, iterations, morse)

    return results


def benchmark_sine_wave_generation(durations: List[float], iterations: int = 10) -> Dict[float, Dict[str, Any]]:
    """
    Benchmark sine wave generation for different durations.
    
    Args:
        durations (List[float]): A list of durations (in seconds) to benchmark.
        iterations (int, optional): The number of iterations for each duration. Defaults to 10.
        
    Returns:
        Dict[float, Dict[str, Any]]: A dictionary mapping durations to benchmark statistics.
    """
    # Use a mocked player to avoid actual audio playback
    import unittest.mock
    with unittest.mock.patch('pygame.mixer.init'):
        player = MorseCodePlayer()

    results = {}

    for duration in durations:
        # Mock pygame.sndarray.make_sound and pygame.mixer.get_init
        with unittest.mock.patch('pygame.sndarray.make_sound'), unittest.mock.patch('pygame.mixer.get_init',
                                                                                    return_value=(44100, -16, 1)):
            results[duration] = run_benchmark(player.create_sine_wave, iterations, duration)

    return results


def print_benchmark_results(title: str, results: Dict[Any, Dict[str, Any]]) -> None:
    """
    Print benchmark results in a formatted table.
    
    Args:
        title (str): The title of the benchmark.
        results (Dict[Any, Dict[str, Any]]): The benchmark results.
    """
    print(f"\n{title}")
    print("-" * 80)
    print(f"{'Input Size':<10} {'Min (s)':<10} {'Max (s)':<10} {'Mean (s)':<10} {'Median (s)':<10} {'StdDev (s)':<10}")
    print("-" * 80)

    for size, stats in sorted(results.items()):
        print(
            f"{size:<10} {stats['min']:<10.6f} {stats['max']:<10.6f} {stats['mean']:<10.6f} {stats['median']:<10.6f} {stats['stdev']:<10.6f}")


def main() -> None:
    """Run all benchmarks and print the results."""
    parser = argparse.ArgumentParser(description="Run performance benchmarks for the Morse Code Converter.")
    parser.add_argument("--iterations", type=int, default=100, help="Number of iterations for each benchmark")
    parser.add_argument("--text-lengths", type=int, nargs="+", default=[10, 50, 100, 500, 1000],
                        help="Text lengths to benchmark")
    parser.add_argument("--durations", type=float, nargs="+", default=[0.01, 0.05, 0.1, 0.5, 1.0],
                        help="Durations to benchmark (in seconds)")
    args = parser.parse_args()

    print("Running benchmarks...")

    # Benchmark text-to-morse conversion
    text_to_morse_results = benchmark_text_to_morse(args.text_lengths, args.iterations)
    print_benchmark_results("Text to Morse Code Conversion", text_to_morse_results)

    # Benchmark morse-to-text conversion
    morse_to_text_results = benchmark_morse_to_text(args.text_lengths, args.iterations)
    print_benchmark_results("Morse Code to Text Conversion", morse_to_text_results)

    # Benchmark sine wave generation
    sine_wave_results = benchmark_sine_wave_generation(args.durations, args.iterations // 10)
    print_benchmark_results("Sine Wave Generation", sine_wave_results)

    print("\nBenchmarks completed.")


if __name__ == "__main__":
    main()
