from recursive_backtracker import RecursiveBacktracker
from grid import Grid

grid = Grid(20,20)
RecursiveBacktracker.mutate(grid)

grid.to_grid()
