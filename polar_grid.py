from grid import Grid
from polar_cell import PolarCell
import math
import random
from PIL import Image, ImageDraw

class PolarGrid(Grid):

    def __init__(self, rows):
        Grid.__init__(self, rows, 1)

    def prepare_grid(self):
        rows = [[PolarCell(0,0)]]
        row_height = 1/self.rows

        for row in range(1,self.rows):
            rows.append([])

            radius = row / self.rows
            circumference = 2 * math.pi * radius

            previous_count = len(rows[row - 1])
            estimated_cell_width = circumference / previous_count
            ratio = int(estimated_cell_width / row_height)

            cells = previous_count * ratio
            for col in range(cells):
                rows[row].append(PolarCell(row, col))
        return rows

    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.column
            row_length = len(self.grid[row])
            if row > 0:
                cell.cw = self.grid[row][(col + 1) % row_length]
                cell.ccw = self.grid[row][col - 1]

                ratio = int(len(self.grid[row]) / len(self.grid[row - 1]))

                parent = self.grid[row - 1][int(col / ratio)]
                parent.outward.append(cell)
                cell.inward = parent

    def random_cell(self):
        row = random.choice(self.grid)
        return random.choice(row)

    def to_png(self, cell_size=30, index = "0"):
        img_size = 2 * self.rows * cell_size
        margin = 10

        background = "#fff"
        wall = "#000"

        center = img_size / 2 + margin
        im = Image.new('RGB', (img_size + 2 * margin, img_size + 2 * margin),(255,255,255))

        draw = ImageDraw.Draw(im)

        for cell in self.each_cell():
            if cell.row == 0: continue

            theta = 2 * math.pi / len(self.grid[cell.row])
            inner_radius = cell.row * cell_size
            outer_radius = inner_radius + cell_size
            theta_ccw = cell.column * theta
            theta_cw = theta_ccw + theta

            ax = ay = bx = by = cx = cy = dx = dy = center
            ax += int(inner_radius * math.cos(theta_ccw))
            ay += int(inner_radius * math.sin(theta_ccw))
            bx += int(outer_radius * math.cos(theta_ccw))
            by += int(outer_radius * math.sin(theta_ccw))
            cx += int(inner_radius * math.cos(theta_cw))
            cy += int(inner_radius * math.sin(theta_cw))
            dx += int(outer_radius * math.cos(theta_cw))
            dy += int(outer_radius * math.sin(theta_cw))

            if not cell.linked(cell.inward):
                draw.arc((center - inner_radius, center - inner_radius, center + inner_radius, center + inner_radius), math.degrees(theta_ccw), math.degrees(theta_cw), fill=wall)
            if not cell.linked(cell.cw):
                draw.line((cx, cy, dx, dy), fill=wall)
        draw.ellipse((margin,margin,img_size + margin, img_size + margin), outline=wall)
        im.save("./exports/polar_maze"+index+".png", "PNG")
