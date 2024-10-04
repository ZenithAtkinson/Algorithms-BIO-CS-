# convex_hull.py

from typing import List, Tuple

def compute_hull(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Computes the convex hull of a set of 2D points using the Divide and Conquer algorithm.

    Args:
        points (List[Tuple[float, float]]): A list of (x, y) tuples representing the points.

    Returns:
        List[Tuple[float, float]]: The convex hull as a list of points in counter-clockwise order.
    """

    # Edge Cases: No points or a single point
    if not points:
        return []
    if len(points) == 1:
        return points.copy()

    # Remove duplicate points and sort the points by x-coordinate, then by y-coordinate
    points_sorted = sorted(set(points), key=lambda p: (p[0], p[1]))  # O(n log n)

    def Orientation(p: Tuple[float, float], q: Tuple[float, float], r: Tuple[float, float]) -> int:
        """
        Determines the Orientation of an ordered triplet (p, q, r).

        Returns:
            0 -> Colinear
            1 -> Clockwise
            2 -> CounterClockwise
        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        epsilon = 1e-12
        if abs(val) < epsilon:
            return 0  # Colinear
        elif val > 0:
            return 1  # Clockwise
        else:
            return 2  # CounterClockwise

    def find_rightmost_point(Hull: List[Tuple[float, float]]) -> Tuple[float, float]:
        """
        Returns the rightmost point in the hull. If multiple, returns the topmost.
        """
        return max(Hull, key=lambda p: (p[0], p[1]))

    def find_leftmost_point(Hull: List[Tuple[float, float]]) -> Tuple[float, float]:
        """
        Returns the leftmost point in the hull. If multiple, returns the bottommost.
        """
        return min(Hull, key=lambda p: (p[0], p[1]))

    def get_index(Hull: List[Tuple[float, float]], point: Tuple[float, float]) -> int:
        """
        Returns the index of the given point in the hull.
        """
        for idx, p in enumerate(Hull):
            if p == point:
                return idx
        raise ValueError("Point not found in hull.")

    def find_upper_tangent(Hull_L: List[Tuple[float, float]], Hull_R: List[Tuple[float, float]]) -> Tuple[int, int]:
        """
        Finds the indices of the upper tangent between Hull_L and Hull_R.

        Returns:
            Tuple[int, int]: Indices (i, j) in Hull_L and Hull_R respectively.
        """
        i = get_index(Hull_L, find_rightmost_point(Hull_L))
        j = get_index(Hull_R, find_leftmost_point(Hull_R))

        done = False
        while not done:
            done = True
            # Move i counter-clockwise as long as the tangent is not upper
            while True:
                next_i = (i + 1) % len(Hull_L)
                o = Orientation(Hull_L[i], Hull_R[j], Hull_L[next_i])
                if o == 2:  # CounterClockwise
                    i = next_i
                    done = False
                else:
                    break
            # Move j clockwise as long as the tangent is not upper
            while True:
                prev_j = (j - 1 + len(Hull_R)) % len(Hull_R)
                o = Orientation(Hull_L[i], Hull_R[j], Hull_R[prev_j])
                if o == 1:  # Clockwise
                    j = prev_j
                    done = False
                else:
                    break
        return i, j

    def find_lower_tangent(Hull_L: List[Tuple[float, float]], Hull_R: List[Tuple[float, float]]) -> Tuple[int, int]:
        """
        Finds the indices of the lower tangent between Hull_L and Hull_R.

        Returns:
            Tuple[int, int]: Indices (i, j) in Hull_L and Hull_R respectively.
        """
        i = get_index(Hull_L, find_rightmost_point(Hull_L))
        j = get_index(Hull_R, find_leftmost_point(Hull_R))

        done = False
        while not done:
            done = True
            # Move i clockwise as long as the tangent is not lower
            while True:
                prev_i = (i - 1 + len(Hull_L)) % len(Hull_L)
                o = Orientation(Hull_L[i], Hull_R[j], Hull_L[prev_i])
                if o == 1:  # Clockwise
                    i = prev_i
                    done = False
                else:
                    break
            # Move j counter-clockwise as long as the tangent is not lower
            while True:
                next_j = (j + 1) % len(Hull_R)
                o = Orientation(Hull_L[i], Hull_R[j], Hull_R[next_j])
                if o == 2:  # CounterClockwise
                    j = next_j
                    done = False
                else:
                    break
        return i, j

    def merge_hulls(Hull_L: List[Tuple[float, float]], Hull_R: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Merges two convex hulls into one convex hull.

        Args:
            Hull_L (List[Tuple[float, float]]): Left convex hull.
            Hull_R (List[Tuple[float, float]]): Right convex hull.

        Returns:
            List[Tuple[float, float]]: Merged convex hull.
        """
        # Find upper and lower tangents
        i_upper, j_upper = find_upper_tangent(Hull_L, Hull_R)
        i_lower, j_lower = find_lower_tangent(Hull_L, Hull_R)

        # Initialize merged hull
        merged_hull = []

        # Add points from Hull_L from i_upper to i_lower (inclusive)
        index = i_upper
        merged_hull.append(Hull_L[index])
        while index != i_lower:
            index = (index + 1) % len(Hull_L)
            merged_hull.append(Hull_L[index])

        # Add points from Hull_R from j_lower to j_upper (inclusive)
        index = j_lower
        merged_hull.append(Hull_R[index])
        while index != j_upper:
            index = (index + 1) % len(Hull_R)
            merged_hull.append(Hull_R[index])

        return merged_hull

    def divide_and_conquer(Q_sorted: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Recursively divides the set of points and merges the convex hulls.

        Args:
            Q_sorted (List[Tuple[float, float]]): Sorted list of points.

        Returns:
            List[Tuple[float, float]]: Convex hull as a list of points in counter-clockwise order.
        """
        n = len(Q_sorted)

        # Base Cases
        if n == 1:
            return Q_sorted.copy()
        elif n == 2:
            return Q_sorted.copy()
        elif n == 3:
            p1, p2, p3 = Q_sorted
            o = Orientation(p1, p2, p3)
            if o == 2:
                return [p1, p2, p3]
            elif o == 1:
                return [p1, p3, p2]
            else:
                # Colinear points: return endpoints
                sorted_pts = sorted(Q_sorted, key=lambda p: (p[0], p[1]))
                return [sorted_pts[0], sorted_pts[-1]]

        # Divide
        mid = n // 2
        L = Q_sorted[:mid]
        R = Q_sorted[mid:]

        # Conquer
        Hull_L = divide_and_conquer(L)  # T(n/2)
        Hull_R = divide_and_conquer(R)  # T(n/2)

        # Merge
        merged_hull = merge_hulls(Hull_L, Hull_R)  # O(n)
        return merged_hull

    # Start the divide and conquer process
    convex_hull = divide_and_conquer(points_sorted)  # O(n log n)

    # Ensure the hull is in counter-clockwise order
    def is_counter_clockwise(hull: List[Tuple[float, float]]) -> bool:
        """
        Checks if the hull is in counter-clockwise order.

        Args:
            hull (List[Tuple[float, float]]): Convex hull.

        Returns:
            bool: True if counter-clockwise, False otherwise.
        """
        area = 0.0
        n = len(hull)
        for i in range(n):
            j = (i + 1) % n
            area += (hull[i][0] * hull[j][1]) - (hull[j][0] * hull[i][1])
        return area > 0

    if not is_counter_clockwise(convex_hull):
        convex_hull.reverse()

    return convex_hull
