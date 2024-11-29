from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        path = []

        # DFS implementation
        def dfs(index, curr_total, path):
            if curr_total == target:
                result.append(path[:])  # Append a copy of the current path
                return
            if curr_total > target:
                return
            
            for i in range(index, len(candidates)):
                path.append(candidates[i])
                dfs(index, curr_total + candidates[i], path)
                path.pop()
                index += 1

        dfs(0, 0, path)
        print(result)

the_list = [2,3,6,7]
target = 7
selfer = Solution
Solution.combinationSum(selfer, the_list, target)

