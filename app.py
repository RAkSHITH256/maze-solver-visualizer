from flask import Flask, render_template, request, jsonify
import time
import copy

# Utils
from utils.generate_grid import generate_grid
from utils.carve import carve
from utils.modify import modify

# Algorithms
from algorithms.dfs_maze_solver import dfs_maze_solver
from algorithms.bfs_maze_solver import bfs_maze_solver
from algorithms.dijkstra_maze_solver import dijkstra_maze_solver
from algorithms.astar_maze_solver import astar_maze_solver
from algorithms.aco_maze_solver import aco_maze_solver
from algorithms.ga_maze_solver import ga_maze_solver
from algorithms.pso_maze_solver import pso_maze_solver

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/maze/generate', methods=['GET'])
def api_generate():
    m = int(request.args.get('m', 41))
    n = int(request.args.get('n', 41))
    
    # Ensure odd dimensions
    if m % 2 == 0: m += 1
    if n % 2 == 0: n += 1

    maze = []
    maze = generate_grid(n, m, maze)
    carve(maze)
    modify(maze, m, n)
    
    return jsonify({"maze": maze.tolist(), "m": m, "n": n})

@app.route('/api/maze/solve', methods=['POST'])
def api_solve():
    data = request.json
    maze_data = data.get('maze')
    algorithm = data.get('algorithm', 'dfs')
    m = len(maze_data)
    n = len(maze_data[0]) if m > 0 else 0
    
    start = [1, 1]
    end = [m - 2, n - 2]
    
    # Deep copy just to be safe
    maze = copy.deepcopy(maze_data)
    
    start_time = time.time()
    
    if algorithm == 'dfs':
        dfs_maze_solver(maze, start, end)
    elif algorithm == 'bfs':
        bfs_maze_solver(maze, start, end)
    elif algorithm == 'dijkstra':
        dijkstra_maze_solver(maze, start, end)
    elif algorithm == 'astar':
        astar_maze_solver(maze, start, end)
    elif algorithm == 'aco':
        aco_maze_solver(maze, start, end)
    elif algorithm == 'ga':
        ga_maze_solver(maze, start, end)
    elif algorithm == 'pso':
        pso_maze_solver(maze, start, end)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400
        
    execution_time = time.time() - start_time
    
    return jsonify({
        "maze": maze,
        "time": execution_time,
        "algorithm": algorithm
    })

@app.route('/api/maze/compare', methods=['POST'])
def api_compare():
    data = request.json
    maze_data = data.get('maze')
    m = len(maze_data)
    n = len(maze_data[0]) if m > 0 else 0
    
    start = [1, 1]
    end = [m - 2, n - 2]
    
    algorithms = {
        'dfs': dfs_maze_solver,
        'bfs': bfs_maze_solver,
        'dijkstra': dijkstra_maze_solver,
        'astar': astar_maze_solver,
        'aco': aco_maze_solver,
        'ga': ga_maze_solver,
        'pso': pso_maze_solver
    }
    
    results = {}
    
    for algo_name, solver_func in algorithms.items():
        maze_copy = copy.deepcopy(maze_data)
        start_time = time.time()
        solver_func(maze_copy, start, end)
        exec_time = (time.time() - start_time) * 1000 # convert to ms
        
        # Calculate path length (count of '2')
        path_length = sum(row.count('2') for row in maze_copy)
        
        results[algo_name] = {
            "maze": maze_copy,
            "time": exec_time,
            "pathLength": path_length
        }
        
    return jsonify(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
