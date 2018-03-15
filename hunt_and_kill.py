import random

class HuntAndKill:

    def mutate(grid):
        current = grid.random_cell()

        while current is not None:
            unvisited_neighbors = [cell for cell in current.neighbors() if len(cell.get_links()) == 0]

            if len(unvisited_neighbors) > 0:
                neighbor = random.choice(unvisited_neighbors)
                current.link(neighbor)
                current = neighbor
            else:
                current = None
                for cell in grid.each_cell():
                    visited_neighbors = [cell for cell in cell.neighbors() if len(cell.get_links()) > 0]

                    if len(cell.get_links()) == 0 and len(visited_neighbors) > 0:
                        current = cell

                        neighbor = random.choice(visited_neighbors)
                        current.link(neighbor)
                        break
        return grid
