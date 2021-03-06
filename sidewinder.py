import random
from make_animation import MakeAnimation

class Sidewinder:

    def mutate(grid, animation = False):
        filenames = []
        frame = 0
        for row in grid.grid:
            run = []
            for cell in row:
                run.append(cell)

                at_eastern_boundary = cell.east is None
                at_northern_boundary = cell.north is None

                should_close_out = at_eastern_boundary or (not at_northern_boundary and random.randrange(2) == 0)

                if should_close_out:
                    member = random.choice(run)
                    if member.north:
                        member.link(member.north)
                        if animation:
                            frame += 1
                            grid.to_png(20, str(frame))
                            filenames.append("./exports/maze"+str(frame)+".png")
                    run = []
                else:
                    cell.link(cell.east)
                    if animation:
                        frame += 1
                        grid.to_png(20, str(frame))
                        filenames.append("./exports/maze"+str(frame)+".png")
        if animation:
            MakeAnimation(filenames, 'sidewinder.gif')
