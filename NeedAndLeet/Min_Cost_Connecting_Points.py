from typing import List

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        #Using prims/kruskalls?

        #def calc_distance(point1: List[int], point2: List[int]):
        #    #d = 9 for [2,2] and [3,10]
        #    d = (point1[0] - point2[0]) + (point1[1] - point2[1])
        #    return -d
        #distance = calc_distance(points[1], points[2])
        #print(distance)

        #connections = {}
        edges = []
        #for point in points:
        #    connections[tuple(point)] = {}
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                point1 = tuple(points[i])
                point2 = tuple(points[j])

                distance = abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) #Man distance

                edges.append((point1, point2, distance))

        #Kruskal algorithm start:
        #print(edges)
        edges_sorted = sorted(edges, key=lambda x: x[2])
        #Make Set for Disjoint Set
        points = [tuple(point) for point in points]
        parents = {point: point for point in points}

        #Find function for disjoint set
        def Find(p: tuple):
            if parents[p] != p:
                parents[p] = Find(parents[p])
            return parents[p]
        
        def Union(p1: tuple, p2:tuple): #Use ranks? Not for now
            root1 = Find(p1)
            root2 = Find(p2)
            if root1 == root2:
                print("already connected")
                return
            else:
                parents[root1] = root2
        
        #MST:
        edge_num = 0
        total_cost = 0
        for edge in edges_sorted:
            point1, point2, weight = edge
            r1 = Find(point1)
            r2 = Find(point2)
            if r1 != r2:
                Union(point1, point2)
                total_cost += weight
                edge_num += 1
                if edge_num == len(points) - 1:
                    break
        
        return total_cost
            



graph = [[0,0],[2,2],[3,10],[5,2],[7,0]]
graph_instance = Solution()
result = graph_instance.minCostConnectPoints(graph)
print(result)