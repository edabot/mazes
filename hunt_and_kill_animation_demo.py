from grid import Grid
from hunt_and_kill import HuntAndKill

grid = Grid(15,15)
HuntAndKill.mutate(grid, True)

grid.to_string()
grid.to_svg()
grid.to_png()
