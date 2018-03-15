class Distances:
    def __init__(self, root):
        self.root = root
        self.cells = {}
        self.cells[root] = 0

    def get_cells(self):
        return self.cells.keys()

    def get(self, cell):
        if cell in self.cells:
            return self.cells[cell]
        else:
            return None

    def set(self, cell, distance):
        self.cells[cell] = distance

    def path_to(self, goal):
        current = goal
        breadcrumbs = Distances(self.root)
        breadcrumbs.cells[current] = self.cells[current]

        while not current == self.root:
            for neighbor in current.get_links():
                if self.cells[neighbor] < self.cells[current]:
                    breadcrumbs.cells[neighbor] = self.cells[neighbor]
                    current = neighbor
                    break

        return breadcrumbs

    def max(self):
        max_distance = 0
        max_cell = self.root

        for cell in self.cells:
            if self.cells[cell] > max_distance:
                max_distance = self.cells[cell]
                max_cell = cell

        return [max_cell, max_distance]
