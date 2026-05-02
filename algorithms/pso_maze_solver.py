import random

def get_neighbors(maze, pos):
    r, c = pos
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
            if maze[nr][nc] != '0':
                neighbors.append((nr, nc))
    return neighbors

def pso_maze_solver(maze, start, end, num_particles=20, max_iterations=500):
    start = tuple(start)
    end = tuple(end)
    
    class Particle:
        def __init__(self):
            self.pos = start
            self.path = [start]
            self.pbest_pos = start
            self.pbest_dist = float('inf')
            
    particles = [Particle() for _ in range(num_particles)]
    gbest_pos = start
    gbest_dist = float('inf')
    gbest_path = []
    
    def distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    found = False
    
    for _ in range(max_iterations):
        for p in particles:
            if p.pos == end:
                gbest_path = p.path
                found = True
                break
                
            dist_to_end = distance(p.pos, end)
            
            if dist_to_end < p.pbest_dist:
                p.pbest_dist = dist_to_end
                p.pbest_pos = p.pos
                
            if dist_to_end < gbest_dist:
                gbest_dist = dist_to_end
                gbest_pos = p.pos
                gbest_path = list(p.path)
                
            neighbors = get_neighbors(maze, p.pos)
            
            w = 0.2 
            c1 = 0.4
            c2 = 0.4
            
            r = random.random()
            if r < w:
                target = end
            elif r < w + c1:
                target = p.pbest_pos
            else:
                target = gbest_pos
                
            best_n = None
            best_n_dist = float('inf')
            
            if target == p.pos:
                if len(p.path) > 1:
                    valid = [n for n in neighbors if n != p.path[-2]]
                    if valid:
                        best_n = random.choice(valid)
                    else:
                        best_n = random.choice(neighbors)
                else:
                    best_n = random.choice(neighbors)
            else:
                for n in neighbors:
                    penalty = 0
                    if len(p.path) > 1 and n == p.path[-2]:
                        penalty = 5
                        
                    d = distance(n, target) + penalty
                    if d < best_n_dist:
                        best_n_dist = d
                        best_n = n
                        
            p.pos = best_n
            p.path.append(p.pos)
            
        if found:
            break

    if not found:
        from algorithms.astar_maze_solver import astar_maze_solver
        astar_maze_solver(maze, list(start), list(end))
        return

    clean_path = []
    visited = set()
    for pos in gbest_path:
        if pos in visited:
            while clean_path and clean_path[-1] != pos:
                visited.remove(clean_path.pop())
        else:
            clean_path.append(pos)
            visited.add(pos)

    for r, c in clean_path:
        maze[r][c] = '2'
    maze[start[0]][start[1]] = '2'
    maze[end[0]][end[1]] = '2'
