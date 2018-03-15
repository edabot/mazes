import random
from make_animation import MakeAnimation

class BinaryTree:

    def mutate(grid, animation = False):
        filenames = []
        frame = 0
        for cell in grid.each_cell():
            neighbors = []
            if cell.north: neighbors.append(cell.north)
            if cell.east: neighbors.append(cell.east)

            if len(neighbors) > 0:
                index = random.randrange(len(neighbors))
                neighbor = neighbors[index]
                cell.link(neighbor)
                if animation:
                    frame += 1
                    grid.to_png(20, str(frame))
                    filenames.append("./exports/maze"+str(frame)+".png")
        if animation:
            MakeAnimation(filenames, 'binary_tree.gif')
