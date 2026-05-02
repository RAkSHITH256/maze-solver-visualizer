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

def ga_maze_solver(maze, start, end, population_size=20, max_generations=50):
    start = tuple(start)
    end = tuple(end)
    
    def random_walk(path, steps):
        curr = path[-1]
        for _ in range(steps):
            if curr == end:
                break
            neighbors = get_neighbors(maze, curr)
            if len(path) > 1:
                valid = [n for n in neighbors if n != path[-2]]
                if valid:
                    curr = random.choice(valid)
                else:
                    curr = random.choice(neighbors)
            else:
                curr = random.choice(neighbors)
            path.append(curr)
        return path

    def fitness(path):
        dist = abs(path[-1][0] - end[0]) + abs(path[-1][1] - end[1])
        loops = len(path) - len(set(path))
        return 1.0 / (dist + 1.0 + loops * 5)
        
    population = [[start] for _ in range(population_size)]
    for i in range(population_size):
        population[i] = random_walk(population[i], 10)
        
    best_path = None
    
    for gen in range(max_generations):
        pop_fitness = [(path, fitness(path)) for path in population]
        pop_fitness.sort(key=lambda x: x[1], reverse=True)
        
        if pop_fitness[0][0][-1] == end:
            best_path = pop_fitness[0][0]
            break
            
        elite_count = max(2, population_size // 5)
        elite = [p[0] for p in pop_fitness[:elite_count]]
        
        new_population = list(elite)
        
        while len(new_population) < population_size:
            p1 = random.choice(elite)
            p2 = random.choice(elite)
            
            intersect = set(p1) & set(p2)
            if intersect and len(intersect) > 1:
                cross_point = random.choice(list(intersect))
                idx1 = p1.index(cross_point)
                idx2 = p2.index(cross_point)
                child = p1[:idx1] + p2[idx2:]
            else:
                child = list(p1)
                
            if random.random() < 0.5:
                child = random_walk(child, random.randint(1, 5))
                
            new_population.append(child)
            
        population = new_population

    if not best_path:
        from algorithms.astar_maze_solver import astar_maze_solver
        astar_maze_solver(maze, list(start), list(end))
        return
        
    clean_path = []
    visited = set()
    for pos in best_path:
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
