from typing import List

class Solution:
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        sorted_pps = sorted(people, key=lambda x: (-x[0], x[1]))
        #print(min(sorted_pps))
        print(sorted_pps)
        final = []
        for i in range(len(sorted_pps)):
            #print(sorted_pps[i][1])
            final.insert(sorted_pps[i][1], sorted_pps[i])

        #print(final)
        return(final)





peoples = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
queue_instance = Solution()
result = queue_instance.reconstructQueue(peoples)
print(result)