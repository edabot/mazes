import random
from make_animation import MakeAnimation

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
            MakeAnimation(filenames, 'recursive_backtracker.gif')

class RecursiveBacktrackerPolar:
    def mutate(grid):
        stack = [grid.center_cell()]

        while len(stack) > 0:
            current = stack[-1]
            next_distance = current.distance + 1
            neighbors = [cell for cell in current.neighbors() if len(cell.get_links()) == 0]
            if len(neighbors) == 0:
                stack.pop()
            else:
                neighbor = random.choice(neighbors)
                current.link(neighbor)
                neighbor.link(current)
                neighbor.set_distance(next_distance)
                stack.append(neighbor)
