from colored_grid import ColoredGrid
from binary_tree import BinaryTree

grid = ColoredGrid(35,35)
BinaryTree.mutate(grid)

start = grid.grid[12][12]

grid.distances = start.distances()

grid.maximum = grid.distances.max()[1]

grid.to_grid()
