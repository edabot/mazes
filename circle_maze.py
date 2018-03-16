from polar_grid import PolarGrid
from recursive_backtracker import RecursiveBacktracker

grid = PolarGrid(8)
RecursiveBacktracker.mutate(grid, True)

grid.to_png()
