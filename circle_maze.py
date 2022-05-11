from polar_grid import PolarGrid
from recursive_backtracker import RecursiveBacktrackerPolar

grid = PolarGrid(22)
RecursiveBacktrackerPolar.mutate(grid)
grid.to_svg_contour()
grid.to_svg_contour(10, True)