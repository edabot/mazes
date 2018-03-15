from grid import Grid
from hunt_and_kill import HuntAndKill

grid = Grid(20,20)
HuntAndKill.mutate(grid)

grid.to_grid()
