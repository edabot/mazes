from grid import Grid
import math
from PIL import Image, ImageDraw

class PolarGrid(Grid):

    def to_png(self, cell_size=30, index = "0"):
        img_size = 2 * self.rows * cell_size
        margin = 10

        background = "#fff"
        wall = "#000"

        center = img_size / 2 + margin
        im = Image.new('RGB', (img_size + 2 * margin, img_size + 2 * margin),(255,255,255))

        draw = ImageDraw.Draw(im)

        for cell in self.each_cell():
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

            if not cell.linked(cell.north):
                draw.arc((center - inner_radius, center - inner_radius, center + inner_radius, center + inner_radius), theta_cw, theta_ccw, fill=wall)
            if not cell.linked(cell.east):
                draw.line((cx, cy, dx, dy), fill=wall)
        draw.ellipse((margin,margin,img_size + margin, img_size + margin), outline=wall)
        im.save("./exports/polar_maze"+index+".png", "PNG")
