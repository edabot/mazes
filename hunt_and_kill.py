import random
from make_animation import MakeAnimation

class HuntAndKill:

    def mutate(grid, animation = False, cell_size=20, fps=10):
        start = current = grid.random_cell()
        index = 0
        filenames = []

        while current is not None:
            unvisited_neighbors = [cell for cell in current.neighbors() if len(cell.get_links()) == 0]

            if len(unvisited_neighbors) > 0:
                neighbor = random.choice(unvisited_neighbors)
                current.link(neighbor)
                current = neighbor
                index += 1
                if animation:
                    grid.distances = start.distances()
                    grid.maximum = grid.distances.max()[1]
                    grid.to_png(cell_size, str(index))
                    filenames.append("./exports/maze"+str(index)+".png")
            else:
                current = None
                for cell in grid.each_cell():
                    visited_neighbors = [cell for cell in cell.neighbors() if len(cell.get_links()) > 0]

                    if len(cell.get_links()) == 0 and len(visited_neighbors) > 0:
                        current = cell

                        neighbor = random.choice(visited_neighbors)
                        current.link(neighbor)
                        index += 1
                        if animation:
                            grid.distances = start.distances()
                            grid.maximum = grid.distances.max()[1]
                            grid.to_png(cell_size, str(index))
                            filenames.append("./exports/maze"+str(index)+".png")
                        break
        if animation:
            MakeAnimation(filenames, 'hunt_and_kill.gif', fps)
