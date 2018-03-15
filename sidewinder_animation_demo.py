import grid
import sidewinder

grid = grid.Grid(15,15)
sidewinder.Sidewinder.mutate(grid, True)
grid.to_string()
grid.to_svg()
