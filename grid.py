from cell import Cell
import random
import svgwrite

class Grid:
    def __init__(self, rows, columns):
        self.rows, self.columns = rows, columns
        self.grid = self.prepare_grid()
        self.configure_cells()

    def prepare_grid(self):
        grid_array = []
        for row in range(self.rows):
            row_array = []
            for column in range(self.columns):
                row_array.append(Cell(row, column))
            grid_array.append(row_array)
        return grid_array

    def configure_cells(self):
        for row in self.grid:
            for cell in row:
                row, col = cell.row, cell.column
                cell.north = self.get_neighbor(row - 1, col)
                cell.south = self.get_neighbor(row + 1, col)
                cell.west = self.get_neighbor(row, col - 1)
                cell.east = self.get_neighbor(row, col + 1)

    def get_neighbor(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self.grid[row][column]
        return None

    def random_cell(self):
        return self.grid[random.randrange(self.rows)][random.randrange(self.columns)]

    def size(self):
        return self.rows * self.columns

    def each_row(self):

        for row in self.grid:
            yield row

    def each_cell(self):
        cells = []
        for row in self.grid:
            for cell in row:
                cells.append(cell)
        return cells

    def contents_of(self, cell):
        return " "

    def background_color_for(self, cell):
        return None

    def to_string(self):
        print("+" + "---+" * self.columns)
        for row in self.grid:
            top = '|'
            bottom='+'

            for cell in row:
                body=" " + self.contents_of(cell) + " "
                east_boundary =  " " if cell.linked(cell.east) else "|"
                top = top + body + east_boundary
                south_boundary = "   " if cell.linked(cell.south) else '---'
                corner = '+'
                bottom = bottom + south_boundary + corner
            print(top)
            print(bottom)

    def to_svg(self, cell_size = 10):

        top_offset = 20
        left_offset = 20
        img_width = cell_size * self.columns
        img_height = cell_size * self.rows
        dwg = svgwrite.Drawing('maze.svg')

        for cell in self.each_cell():
            x1 = cell.column * cell_size + top_offset
            y1 = cell.row * cell_size + left_offset
            x2 = (cell.column + 1) * cell_size + top_offset
            y2 = (cell.row + 1) * cell_size + left_offset
            dwg.add(dwg.text(self.contents_of(cell), insert=(x1 + 5 ,y1 + cell_size - 5)))

            if self.background_color_for(cell) is not None:
                dwg.add(dwg.rect(insert=(x1, y1), size=(cell_size, cell_size), rx=None, ry=None, fill=self.background_color_for(cell)))

            if not cell.north:
                dwg.add(dwg.line((x1, y1), (x2, y1), stroke=svgwrite.rgb(10, 10, 16, '%')))
            if not cell.west:
                dwg.add(dwg.line((x1, y1), (x1, y2), stroke=svgwrite.rgb(10, 10, 16, '%')))

            if not cell.linked(cell.east):
                dwg.add(dwg.line((x2, y1), (x2, y2), stroke=svgwrite.rgb(10, 10, 16, '%')))
            if not cell.linked(cell.south):
                dwg.add(dwg.line((x1, y2), (x2, y2), stroke=svgwrite.rgb(10, 10, 16, '%')))
        dwg.save()
