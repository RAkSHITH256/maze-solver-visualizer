import random
from utils.get_neighbours_for_search import get_neighbours_for_search

def dfs_maze_solver(maze, start, end):
  """
  It takes a maze, a start and an end, and returns a solved maze
  
  :param maze: The maze to be solved
  :param start: The starting point of the maze
  :param end: The end point of the maze
  """
  
  visited = []
  stack = [start]
  path_found = False
  
  while stack:
    actual = stack[-1]
    
    if actual not in visited:
      visited.append(actual)
      
    if actual == end:
      path_found = True
      break
      
    neighbours = get_neighbours_for_search(maze, actual[0], actual[1], visited)
    
    if neighbours:
      neighbour = random.choice(neighbours)
      stack.append(neighbour)
    else:
      stack.pop()

  if path_found:
    for i in range(len(stack)):
      if i < len(stack)-1:
        actual = stack[i]
        next_node = stack[i+1]
        if actual[0] == next_node[0]:
          if actual[1] < next_node[1]:
            maze[actual[0]][actual[1]+1] = '2'
          elif actual[1] > next_node[1]:
            maze[actual[0]][actual[1]-1] = '2'
        elif actual[1] == next_node[1]:
          if actual[0] < next_node[0]:
            maze[actual[0]+1][actual[1]] = '2'
          elif actual[0] > next_node[0]:
            maze[actual[0]-1][actual[1]] = '2'

      maze[stack[i][0]][stack[i][1]] = '2'