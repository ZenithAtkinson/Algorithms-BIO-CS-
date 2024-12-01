class Solution:
    def findMinArrowShots(self, points):
        if not points:
            return 0
        points.sort(key=lambda x: x[1]) #Sorting, based on 2nd val (end)
        #print(points)
        arrow_count = 1
        arrow_position = points[0][1]
        #print(arrow_position)

        for xstart, xend in points:
            if xstart > arrow_position:
                #NEW arow
                arrow_count += 1
                arrow_position = xend
                #print(arrow_position)

        return arrow_count


points = [[10, 16], [2, 8], [1, 6], [7, 12]]
solution = Solution()
result = solution.findMinArrowShots(points)
print(result)