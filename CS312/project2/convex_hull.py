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
    for i in range(rightHullSize):
        # looking for the extreme slopes #
        greatestPositiveSlope = calculateSlope(keyPoint_left, upperTangent_right)
        greatestNegativeSlope = calculateSlope(keyPoint_left, lowerTangent_right)

        if calculateSlope(keyPoint_left, rightHull[i]) > greatestPositiveSlope:
            upperTangent_right = rightHull[i]

        if calculateSlope(keyPoint_left, rightHull[i]) < greatestNegativeSlope:
            lowerTangent_right = rightHull[i]

            

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