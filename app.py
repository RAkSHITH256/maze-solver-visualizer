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
    else:
        return jsonify({"error": "Unknown algorithm"}), 400
        
    execution_time = time.time() - start_time
    
    return jsonify({
        "maze": maze,
        "time": execution_time,
        "algorithm": algorithm
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
