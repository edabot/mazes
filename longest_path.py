from distance_grid import DistanceGrid
from binary_tree import BinaryTree

grid = DistanceGrid(12,12)

BinaryTree.mutate(grid)

start = grid.grid[0][0]

distances = start.distances()
new_start, distance = distances.max()

new_distances = new_start.distances()
goal, distance = new_distances.max()

grid.distances = new_distances.path_to(goal)

grid.to_string()
grid.to_grid()
