from grid import Grid
import base36

class DistanceGrid(Grid):

    def __init__(self, rows, columns):
        self.rows, self.columns = rows, columns
        self.grid = self.prepare_grid()
        self.configure_cells()
        self.distances = {}

    def contents_of(self, cell):
        if self.distances:
            return base36.dumps(self.distances.get(cell))
        else:
            super
