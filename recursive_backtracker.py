import random
import imageio
import os

class RecursiveBacktracker:
    def mutate(grid, animation = False):
        frame = 0
        filenames = []
        stack = []
        stack.append(grid.random_cell())

        while len(stack) > 0:
            current = stack[-1]
            neighbors = [cell for cell in current.neighbors() if len(cell.get_links()) == 0]

            if len(neighbors) == 0:
                stack.pop()
            else:
                neighbor = random.choice(neighbors)
                current.link(neighbor)
                stack.append(neighbor)
                if animation:
                    frame += 1
                    grid.to_png(20, str(frame))
                    filenames.append("./exports/maze"+str(frame)+".png")
        if animation:
            images = []
            for filename in filenames:
                images.append(imageio.imread(filename))
            imageio.mimsave('./exports/recursive_backtracker.gif', images)
            for filename in filenames:
                os.remove(filename)
