import random

class RecursiveBacktracker:
    def mutate(grid):
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
        return grid
