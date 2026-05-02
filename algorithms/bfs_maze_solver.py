import random
from utils.get_neighbours_for_search import get_neighbours_for_search

def bfs_maze_solver(maze, start, end):
  """
  It takes a maze, a start and an end, and it returns a solved maze
  
  :param maze: the maze to be solved
  :param start: (0, 0)
  :param end: The end point of the maze
  """
  
  visited = []
  queue = [start]
  parent = {tuple(start): None}
  path_found = False
  
  while queue:
    actual = queue.pop(0)
    
    if actual not in visited:
      visited.append(actual)
      
    if actual == end:
      path_found = True
      break
      
    neighbours = get_neighbours_for_search(maze, actual[0], actual[1], visited)
    
    for neighbour in neighbours:
      if neighbour not in visited and neighbour not in queue:
        queue.append(neighbour)
        parent[tuple(neighbour)] = actual

  if path_found:
    path = []
    curr = tuple(end)
    while curr is not None:
      path.append(list(curr))
      curr = parent.get(tuple(curr))
    
    path.reverse()
    
    for i in range(len(path)):
      if i < len(path)-1:
        actual = path[i]
        next_node = path[i+1]
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

      maze[path[i][0]][path[i][1]] = '2'