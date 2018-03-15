import random
import imageio

class HuntAndKill:

    def mutate(grid):
        current = grid.random_cell()
        index = 0
        filenames = []

        while current is not None:
            unvisited_neighbors = [cell for cell in current.neighbors() if len(cell.get_links()) == 0]

            if len(unvisited_neighbors) > 0:
                neighbor = random.choice(unvisited_neighbors)
                current.link(neighbor)
                current = neighbor
                index += 1
                grid.to_png(20, str(index))
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
                        grid.to_png(20, str(index))
                        filenames.append("./exports/maze"+str(index)+".png")
                        break
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('movie.gif', images)
