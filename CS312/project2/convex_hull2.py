# Uncomment this line to import some functions that can help
# you debug your algorithm
# from plotting import draw_line, draw_hull, circle_point


def compute_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
            # point A (x,y)                 # point B (x,y)
    # edges = list[tuple[tuple[float, float], tuple[float, float]]]
    """Return the subset of provided points that define the convex hull"""

    # sort the array #
    sortedPoints = sorted(points) # assuming this sorts by x-chords, assuming this is time n * log(n)

    if len(points) <= 3:
        # if there's only three, all are included #
        return sortedPoints

    # split array recursively #
    midpoint = len(points) // 2
    # splitting array in two. start to mid, and mid to end #
    leftHull = compute_hull(sortedPoints[:midpoint])  # left hull
    rightHull = compute_hull(sortedPoints[midpoint:])  # right hull


    # these are the original keypoints, will use them to find the four points that will direct the merge #
    keyPoint_left = leftHull[-1]
    keyPoint_right = rightHull[0]

    # these will be reassigned to be the two points defining the TOP of the merged shape #
    upperTangent_left = leftHull[-1]
    upperTangent_right = rightHull[0]

    # these will be reassigned to be the two points defining the BOTTOM of the merged shape #
    lowerTangent_left = leftHull[-1]
    lowerTangent_right = rightHull[0]

    leftHullSize = len(leftHull)
    rightHullSize = len(rightHull)

    # find the greatest/least slopes (+/-) between the keyPoint on the left and any point within the right hull #
 


    # find the smallest slope (-) between all points on the left and the newly assigned keyPoint on the right hull #
    for i in range(leftHullSize):
        # looking for the extreme slopes using the newly defined upper/lower right tangent points #
        greatestNegativeSlope = calculateSlope(keyPoint_left, upperTangent_right)
        greatestPositiveSlope = calculateSlope(keyPoint_left, lowerTangent_right)
        #these initial values SHOULD be overwritten quickly, their names

        # keypoint left starts as the rightmost, but does not have to stay as that point... prolly shouldn't #
        if calculateSlope(leftHull[i], upperTangent_right) < greatestNegativeSlope:
            upperTangent_left = leftHull[i]

        if calculateSlope(leftHull[i], lowerTangent_right) > greatestPositiveSlope:
            lowerTangent_left = leftHull[i]

    # remove former key points, add in the tangent points #
    sortedPoints.remove(keyPoint_left)
    sortedPoints.remove(keyPoint_right)

    sortedPoints.append(upperTangent_left)
    sortedPoints.append(upperTangent_right)
    sortedPoints.append(lowerTangent_left)
    sortedPoints.append(lowerTangent_right)

    # secure the tuples
    return sortedPoints

def calculateSlope(left: tuple[float, float], right: tuple[float, float]):
    rise = right[1] - left[1] # right's Y chord - left's Y chord
    run = right[0] - left[0] # right's X chord - left's X chord
    return rise/run


#L is equal to our left hull
#R is equal to our right hull
def find_upper_tangent(L, R):
    # Find the rightmost point in L and the leftmost point in R
    pperTangent_left = L[-1]   # Rightmost point of left hull
    upperTangent_right = R[0]  
    
    def is_upper_tangent(p, q, L):
        # Check if line pq is the upper tangent to L
        idx_p = L.index(p)
        prev_p = L[idx_p - 1] if idx_p > 0 else L[-1]
        next_p = L[(idx_p + 1) % len(L)]
        return (cross_product(p, q, prev_p) >= 0 and cross_product(p, q, next_p) >= 0)

    def cross_product(o, a, b):
        # Cross product of vectors OA and OB
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    done = False
    while not done:
        done = True
        
        # Move p counterclockwise in L while pq is not an upper tangent to L
        while not is_upper_tangent(p, q, L):
            p_idx = L.index(p)
            p = L[(p_idx - 1) % len(L)]  # Move counterclockwise in L
            done = False
        
        # Move q clockwise in R while pq is not an upper tangent to R
        while not is_upper_tangent(q, p, R):  # Here we reverse the order to check tangent on R
            q_idx = R.index(q)
            q = R[(q_idx + 1) % len(R)]  # Move clockwise in R
            done = False

    return (p, q)

# Example input convex hulls (list of points) L and R
L = [(1, 1), (2, 3), (3, 4), (4, 2)]
R = [(5, 2), (6, 3), (7, 1)]

upper_tangent = find_upper_tangent(L, R)
print("Upper Tangent Points:", upper_tangent)
