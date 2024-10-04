import argparse
from time import time
from typing import List, Tuple
import statistics
import matplotlib.pyplot as plt

from generate import generate_random_points
from convex_hull import compute_hull
from plotting import plot_points, draw_hull, title, show_plot

def main(n: int, distribution: str, seed: int | None):
    points = generate_random_points(distribution, n, seed)
    plot_points(points)

    start = time()
    hull_points = compute_hull(points)
    end = time()

    draw_hull(hull_points)
    title(f'{n} {distribution} points: {round(end - start, 4)} seconds')
    show_plot()


def run_experiments():
    """
    Runs experiments to evaluate the performance of the compute_hull function.
    Generates datasets of varying sizes, measures execution times, and plots the results.
    """
    # Define dataset sizes (adjust as needed)
    dataset_sizes = [10, 100, 1000, 5000, 10000, 50000, 100000]
    runs_per_size = 5  # Number of runs per dataset size for averaging
    execution_times = []  # To store mean execution times for each dataset size

    for n in dataset_sizes:
        print(f"\nGenerating {n} random points...")
        points = generate_random_points('uniform', n, seed=None)  # You can vary the distribution if needed

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

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, execution_times, marker='o', linestyle='-', color='b', label=' Time')
    plt.title('Divide and Conquer Convex Hull Algorithm Performance')
    plt.xlabel('Number of Points (n)')
    plt.ylabel(' Time (seconds)')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig('execution_time_plot.png')  # Save the plot as a PNG file
    plt.show()

if __name__ == '__main__':

    # To debug or run in your IDE
    # you can uncomment the lines below and modify the arguments as needed
    # import sys
    # sys.argv = ['main.py', '-n', '10', '--seed', '312', '--debug']

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='The number of points to generate', default=10)
    parser.add_argument('-d', '--dist', '--distribution',
                        help='The distribution from which to generate points',
                        default='uniform'
                        )
    parser.add_argument('--seed', type=int, default=None, help="Random seed")
    parser.add_argument('--debug', action='store_true', help='Turn on debug plotting')
    parser.add_argument('--experiment', action='store_true', help='Run experimental evaluation')  # New argument
    args = parser.parse_args()

    if args.debug:
        # To debug your algorithm with incremental plotting:
        # - run this script with --debug (e.g. add '--debug' to the sys.argv above)
        # - set breakpoints
        # As you step through your code, you will see the plot update as you go
        import matplotlib.pyplot as plt
        plt.switch_backend('QtAgg')
        plt.ion()

    if args.experiment:
        run_experiments()
    else:
        main(args.n, args.dist, args.seed)
