from recursive_backtracker import RecursiveBacktracker
from grid import Grid

grid = Grid(15,15)
RecursiveBacktracker.mutate(grid, True)

grid.to_string()
grid.to_svg()
