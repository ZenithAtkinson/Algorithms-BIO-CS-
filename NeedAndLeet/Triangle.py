from typing import List

class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        if len(triangle) == 1:
            print("only val")
            return triangle[0][0]
        
        tri_copy = triangle.copy()
        
        for row in range(len(triangle) - 2, -1, -1):
            for col in range(len(triangle[row])):
                val1 = tri_copy[row+1][col]
                val2 = tri_copy[row+1][col+1]
                tri_copy[row][col] += min(val1, val2)
        
        min2 = tri_copy[0][0]
        return min2


triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
triangle_instance = Solution()
result = triangle_instance.minimumTotal(triangle)
print(result)