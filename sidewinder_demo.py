import grid
import sidewinder

grid = grid.Grid(20,20)
sidewinder.Sidewinder.mutate(grid)
grid.to_string()
grid.to_svg()
