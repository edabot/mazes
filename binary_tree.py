import random

class BinaryTree:

    def mutate(grid):
        for cell in grid.each_cell():
            neighbors = []
            if cell.north: neighbors.append(cell.north)
            if cell.east: neighbors.append(cell.east)

            if len(neighbors) > 0:
                index = random.randrange(len(neighbors))
                neighbor = neighbors[index]
                cell.link(neighbor)
