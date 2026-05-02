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

def aco_maze_solver(maze, start, end, num_ants=10, iterations=5):
    start = tuple(start)
    end = tuple(end)
    pheromones = {}
    
    def get_pheromone(pos):
        return pheromones.get(pos, 1.0)
    
    def distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    best_path = None
    best_length = float('inf')

    for _ in range(iterations):
        paths = []
        for _ in range(num_ants):
            path = [start]
            visited = set([start])
            current = start
            stack = [start]
            
            while current != end:
                neighbors = get_neighbors(maze, current)
                unvisited = [n for n in neighbors if n not in visited]
                
                if not unvisited:
                    if stack:
                        stack.pop()
                        if stack:
                            current = stack[-1]
                            path.append(current)
                        else:
                            break
                    else:
                        break
                    continue
                
                probs = []
                total = 0
                for n in unvisited:
                    p = get_pheromone(n)
                    h = 1.0 / (distance(n, end) + 1)
                    val = (p ** 1.0) * (h ** 2.0)
                    probs.append(val)
                    total += val
                
                if total == 0:
                    probs = [1.0/len(unvisited)] * len(unvisited)
                else:
                    probs = [p/total for p in probs]
                
                r = random.random()
                cumulative = 0
                next_node = unvisited[-1]
                for i, p in enumerate(probs):
                    cumulative += p
                    if r <= cumulative:
                        next_node = unvisited[i]
                        break
                
                current = next_node
                visited.add(current)
                path.append(current)
                stack.append(current)
                
            if current == end:
                clean_path = list(stack)
                paths.append(clean_path)
                if len(clean_path) < best_length:
                    best_length = len(clean_path)
                    best_path = clean_path
                    
        for pos in pheromones:
            pheromones[pos] *= 0.9
            
        for p in paths:
            deposit = 100.0 / len(p)
            for pos in p:
                pheromones[pos] = get_pheromone(pos) + deposit

    if best_path:
        for r, c in best_path:
            maze[r][c] = '2'
        maze[start[0]][start[1]] = '2'
        maze[end[0]][end[1]] = '2'
    else:
        from algorithms.dfs_maze_solver import dfs_maze_solver
        dfs_maze_solver(maze, list(start), list(end))
