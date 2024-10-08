import argparse
from time import time
import statistics
import matplotlib.pyplot as plt
import numpy as np

from generate import generate_random_points
from convex_hull import compute_hull

def run_experiments():
    """
    Runs experiments to evaluate the performance of the compute_hull function.
    Generates datasets of varying sizes, measures execution times, and plots the results.
    """
    # Define dataset sizes (adjust as needed)
    dataset_sizes = [10, 100, 1000, 10000, 50000, 100000, 500000, 1000000]
    runs_per_size = 5  # Number of runs per dataset size for averaging
    execution_times = []  # To store mean execution times for each dataset size

    for n in dataset_sizes:
        print(f"\nGenerating {n} random points...")
        points = generate_random_points('uniform', n, seed=None)

        print(f"Measuring execution time for {n} points over {runs_per_size} runs...")
        times = []  # To store execution times for current dataset size

        for run in range(1, runs_per_size + 1):
            start_time = time()
            hull_points = compute_hull(points)
            end_time = time()
            elapsed_time = end_time - start_time
            times.append(elapsed_time)
            print(f"Run {run}: {elapsed_time:.6f} seconds")

        mean_time = statistics.mean(times)
        execution_times.append(mean_time)
        print(f"Mean execution time for {n} points: {mean_time:.6f} seconds")

    # Convert lists to numpy arrays for calculations
    n_values = np.array(dataset_sizes)
    execution_times = np.array(execution_times)

    # Compute theoretical time complexities (without scaling constants)
    t_n_log_n = n_values * np.log(n_values)
    t_n = n_values
    t_n_squared = n_values ** 2
    t_log_n = np.log(n_values)

    # Scaling factors to make the theoretical curves pass through the first data point
    c_n_log_n = execution_times[0] / t_n_log_n[0]
    c_n = execution_times[0] / t_n[0]
    c_n_squared = execution_times[0] / t_n_squared[0]
    c_log_n = execution_times[0] / t_log_n[0]

    # Debugging: Print the scaling factors to verify
    print(f"Scaling Factors: \nO(n log n): {c_n_log_n}, O(n): {c_n}, O(n²): {c_n_squared}, O(log n): {c_log_n}")

    # Scaled theoretical times
    y_n_log_n = c_n_log_n * t_n_log_n
    y_n = c_n * t_n
    y_n_squared = c_n_squared * t_n_squared
    y_log_n = c_log_n * t_log_n

    # Check if any scaling values are too large or too small
    print(f"y_n_log_n: {y_n_log_n}")
    print(f"y_n_squared: {y_n_squared}")

    # Plotting the results with adjusted y-axis limits
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, execution_times, marker='o', linestyle='-', color='b', label='Measured Time')
    plt.plot(n_values, y_n_log_n, linestyle='--', label='O(n log n)')
    plt.plot(n_values, y_n, linestyle='--', label='O(n)')
    plt.plot(n_values, y_n_squared, linestyle='--', label='O(n²)')
    plt.plot(n_values, y_log_n, linestyle='--', label='O(log n)')

    # Dynamically set the y-axis limit based on data
    plt.ylim(min(execution_times) * 0.1, max(y_n_squared) * 1.1)  # Adjust based on data range

    plt.title('Divide and Conquer Convex Hull Algorithm Performance')
    plt.xlabel('Number of Points (n)')
    plt.ylabel('Time (seconds)')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig('execution_time_plot.png')  # Save the plot as a PNG file
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment', action='store_true', help='Run experimental evaluation')
    args = parser.parse_args()

    if args.experiment:
        run_experiments()
