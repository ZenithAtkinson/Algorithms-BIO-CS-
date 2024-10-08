from typing import List, Tuple

def compute_hull(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:

    points.sort()  # Sorting
    unique_points = [] # Removing the dupes
    for point in points:
        if len(unique_points) == 0 or unique_points[-1] != point:
            unique_points.append(point)
    points = unique_points

    # Base case: if less than or equal to 1 point, just return it (there cant be a convex hull if theres just 1 point dug)
    if len(points) <= 1:
        return points
     #Edge Cases: no points or a single point
    #if not points:
    #    return []
    #if len(points) == 1:
    #    return points.copy()

    points.sort() #Sort for horizontal vals
    
    # left and right halves
    mid = len(points) // 2
     #print(mid) 
    l_points = points[:mid]
    r_points = points[mid:]
    #print(l_points) 
    #print(r_points)

    # Recursively for both
    l_hull = compute_hull(l_points)
    r_hull = compute_hull(r_points)

    #index = i_upper
        #merged_hull.append(Hull_L[index])
    return merge_hulls(l_hull, r_hull)


#Look into using grahams
def merge_hulls(left_hull: List[Tuple[float, float]], right_hull: List[Tuple[float, float]]):
    up_l, up_R = find_upper_tangent(left_hull, right_hull)
    lower_L, lower_R = find_lower_tangent(left_hull, right_hull)
    merged_hull = []
    
    # lower_left -> up_left on left (clockwise)
    clock_hand = lower_L
    merged_hull.append(left_hull[clock_hand])
    while clock_hand != up_l:
        clock_hand = (clock_hand + 1) % len(left_hull)
        merged_hull.append(left_hull[clock_hand])
    
    # up_right -> lower_right on right (clockwise )
    clock_hand2 = up_R
    merged_hull.append(right_hull[clock_hand2])
    while clock_hand2 != lower_R:
        clock_hand2 = (clock_hand2 + 1) % len(right_hull)
        merged_hull.append(right_hull[clock_hand2])
    
    return merged_hull

def find_upper_tangent(left_hull: List[Tuple[float, float]], right_hull: List[Tuple[float, float]]):
    # indices to rightmost point of left_hull and leftmost point of right_hull
    #https://www.freecodecamp.org/news/lambda-expressions-in-python/
    #https://codesarray.com/view/Lambda-Functions-in-Python
    leftside = max(range(len(left_hull)), key=lambda i: left_hull[i][0])
    rightside = min(range(len(right_hull)), key=lambda i: right_hull[i][0])
    DONE = False
    while not DONE:
        DONE = True
        #  counterclockwise
        while Orientation(right_hull[rightside], left_hull[leftside], left_hull[(leftside - 1) % len(left_hull)]) > 0:
            # USING MOD, wraps around and makes the list circular (never below 0 or above max length)
            leftside = (leftside - 1) % len(left_hull)
            #print(leftside)
            DONE = False
        # clockwise
        while Orientation(left_hull[leftside], right_hull[rightside], right_hull[(rightside + 1) % len(right_hull)]) < 0:
            # USING MOD, wraps around and makes the list circular (never below 0 or above max length)
            rightside = (rightside + 1) % len(right_hull)
            DONE = False
    return leftside, rightside

def find_lower_tangent(left_hull: List[Tuple[float, float]], right_hull: List[Tuple[float, float]]):
    # indices to rightmost point of left_hull and leftmost point of right_hull
    #https://www.freecodecamp.org/news/lambda-expressions-in-python/
    #https://codesarray.com/view/Lambda-Functions-in-Python
    leftside = max(range(len(left_hull)), key=lambda i: left_hull[i][0])
    rightside = min(range(len(right_hull)), key=lambda i: right_hull[i][0])
    
    done = False
    while not done:
        done = True
        # clockwise
        #i = next_i
        #o = Orientation(left_hull[i], right_hull[j], right_hull[prev_j])
        while Orientation(right_hull[rightside], left_hull[leftside], left_hull[(leftside + 1) % len(left_hull)]) < 0:
            # USING MOD, wraps around and makes the list circular (never below 0 or above max length)
            leftside = (leftside + 1) % len(left_hull)
            #print(leftside)
            done = False
        #  counterclockwise
        while Orientation(left_hull[leftside], right_hull[rightside], right_hull[(rightside - 1) % len(right_hull)]) > 0:
            # USING MOD, wraps around and makes the list circular (never below 0 or above max length)
            rightside = (rightside - 1) % len(right_hull)
            done = False
    return leftside, rightside

def Orientation(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]): # O(1)
    #help from geek for geeks, but basically is positive of p1, p2, p3 are counterclocksise in order
    return (p2[0] - p1[0])*(p3[1] - p1[1]) - (p2[1] - p1[1])*(p3[0] - p1[0])


#def is_counter_clockwise(hull: List[Tuple[float, float]]) -> bool:
#        area = 0
#        n = len(hull)
#        for i in range(n):
#            j = (i + 1) % n
#            area += (hull[i][0] * hull[j][1]) - (hull[j][0] * hull[i][1])
#
#
#        return area > 0
#
#    if not is_counter_clockwise(convex_hull):
#        convex_hull.reverse()
#