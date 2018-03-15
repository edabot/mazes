from grid import Grid
from hunt_and_kill import HuntAndKill

grid = Grid(10,10)
HuntAndKill.mutate(grid)

grid.to_string()
grid.to_svg()
grid.to_png()
