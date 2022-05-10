from polar_grid import PolarGrid
from recursive_backtracker import RecursiveBacktrackerPolar

grid = PolarGrid(10)
RecursiveBacktrackerPolar.mutate(grid)
grid.to_svg()
