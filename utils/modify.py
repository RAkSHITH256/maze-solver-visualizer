import random

def modify(maze, m, n):
  # Remove a proportional number of walls to create many alternative paths
  num_walls_to_remove = (m * n) // 10 
  for i in range(num_walls_to_remove):
    x = random.randint(1, n-2)
    y = random.randint(1, m-2)
    maze[x][y] = '1'