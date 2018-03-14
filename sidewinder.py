import random

class Sidewinder:

    def mutate(grid):
        for row in grid.grid:
            run = []
            for cell in row:
                run.append(cell)

                at_eastern_boundary = cell.east is None
                at_northern_boundary = cell.north is None

                should_close_out = at_eastern_boundary or (not at_northern_boundary and random.randrange(2) == 0)

                if should_close_out:
                    member = random.choice(run)
                    if member.north: member.link(member.north)
                    run = []
                else:
                    cell.link(cell.east)
