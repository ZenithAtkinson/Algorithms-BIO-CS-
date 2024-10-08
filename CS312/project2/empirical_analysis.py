import numpy as np
import time
import matplotlib.pyplot as plt
import argparse
from convex_hull import compute_hull  # Importing the convex hull function
from generate import generate_random_points  # Correct function for point generation

def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description='Empirical Analysis of Convex Hull Algorithm')
    parser.add_argument('--dist', type=str, choices=['normal', 'uniform'], default='uniform',
                        help='Distribution type for generating points (normal or uniform)')
    args = parser.parse_args()
    distribution = args.dist

    # Values of n to test
    n_values = [10, 100, 1000, 10000, 100000, 500000, 1000000]

    # Initialize lists to store results
    mean_times = []
    std_times = []
    proportionality_constants = []

    # Loop through each value of n
    for n in n_values:
        times = []
        
        # Run the experiment 5 times for each n
        for _ in range(5):
            # Generate points using the specified distribution
            points = generate_random_points(distribution, n)
            
            # Measure time to compute convex hull
            start_time = time.perf_counter()
            hull = compute_hull(points)  # Compute convex hull
            end_time = time.perf_counter()
            
            elapsed_time = end_time - start_time
            times.append(elapsed_time)
        
        # Compute the mean and standard deviation of times for this value of n
        mean_time = np.mean(times)
        std_time = np.std(times)
        mean_times.append(mean_time)
        std_times.append(std_time)
        
        # Compute n log n
        n_log_n = n * np.log2(n)
        
        # Compute constant of proportionality k = t / (n log n)
        k = mean_time / n_log_n
        proportionality_constants.append(k)
    
    # Plotting the results (n vs. mean time with error bars)
    plt.figure(figsize=(10, 6))
    plt.errorbar(n_values, mean_times, yerr=std_times, fmt='o', capsize=5)
    plt.xscale('log')  # Logarithmic scale for n
    plt.xlabel('n (Number of points)')
    plt.ylabel('Mean Time (seconds)')
    plt.title('Empirical Analysis: n vs Time for Convex Hull Algorithm')
    plt.grid(True)
    plt.show()

    # Plotting mean time vs n log n
    n_log_n_values = [n * np.log2(n) for n in n_values]
    plt.figure(figsize=(10, 6))
    plt.plot(n_log_n_values, mean_times, marker='o')
    plt.xlabel('n log n')
    plt.ylabel('Mean Time (seconds)')
    plt.title('Empirical Analysis: n log n vs Time for Convex Hull Algorithm')
    plt.grid(True)
    plt.show()

    # Plotting the constant of proportionality k vs n
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, proportionality_constants, marker='o')
    plt.xscale('log')  # Logarithmic scale for n
    plt.xlabel('n (Number of points)')
    plt.ylabel('Proportionality Constant k')
    plt.title('Constant of Proportionality k vs n')
    plt.grid(True)
    plt.show()

    # Print the constants of proportionality
    print("Constants of Proportionality (k) for each n:")
    for n, k in zip(n_values, proportionality_constants):
        print(f'n = {n}, k = {k}')

if __name__ == "__main__":
    main()
