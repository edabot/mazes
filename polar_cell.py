from cell import Cell


class PolarCell(Cell):
    def __init__(self, row, column):
        Cell.__init__(self, row, column)
        self.outward = []

    def neighbors(self):
        list = []
        if self.cw: list.append(self.cw)
        if self.ccw: list.append(self.ccw)
        if self.inward: list.append(self.inward)
        if self.outward: list += self.outward
        return list
        
