class Distances:
    def __init__(self, root):
        self.root = root
        self.cells = {}
        self.cells[root] = 0

    def cells(self):
        return self.cells.keys()

    def get(self, cell):
        return self.cells[cell]

    def set(self, cell, distance):
        self.cells[cell] = distance
