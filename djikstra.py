from distance_grid import DistanceGrid
from binary_tree import BinaryTree

grid = DistanceGrid(12,12)
BinaryTree.mutate(grid)

start = grid.grid[0][0]
finish = grid.grid[11][0]
distances = start.distances()

grid.distances = distances

grid.to_string()

grid.distances = distances.path_to(finish)

grid.to_string()
