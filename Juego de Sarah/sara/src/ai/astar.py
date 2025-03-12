from heapq import heappush, heappop

class AStar:
    def __init__(self):
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
    def find_path(self, start, goal, grid):
        frontier = []
        heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        while frontier:
            current = heappop(frontier)[1]
            
            if current == goal:
                break
                
            for dx, dy in self.directions:
                next_pos = (current[0] + dx, current[1] + dy)
                
                if self.is_valid(next_pos, grid):
                    new_cost = cost_so_far[current] + 1
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        priority = new_cost + self.heuristic(next_pos, goal)
                        heappush(frontier, (priority, next_pos))
                        came_from[next_pos] = current
        
        return self.reconstruct_path(came_from, start, goal)
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def is_valid(self, pos, grid):
        return (0 <= pos[0] < len(grid) and 
                0 <= pos[1] < len(grid[0]) and 
                grid[pos[0]][pos[1]] == 0)
    
    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        
        return path 