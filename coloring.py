from colored_grid import ColoredGrid
from sidewinder import Sidewinder

height, width = [50, 50]

grid = ColoredGrid(height,width)
Sidewinder.mutate(grid)

start = grid.grid[int(height/2)][int(width/2)]

grid.distances = start.distances()

grid.maximum = grid.distances.max()[1]

grid.to_grid()
