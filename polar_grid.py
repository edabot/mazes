from unittest import skip
from grid import Grid
from polar_cell import PolarCell
import math
import random
from PIL import Image, ImageDraw
import svgwrite

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

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

    def center_cell(self):
        return self.grid[0][0]     

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
        im.save("./exports/maze"+index+".png", "PNG")

    def to_svg(self, cell_size = 10):

        img_size = 2 * self.rows * cell_size
        margin = 10
        center = img_size / 2 + margin
        dwg = svgwrite.Drawing('./exports/polarmaze.svg')

        for cell in self.each_cell():
            if cell.row == 0: continue

            theta = 2 * math.pi / len(self.grid[cell.row])
            inner_radius = cell.row * cell_size
            center_radius_inner = (cell.row - .5) * cell_size
            center_radius = (cell.row + .5) * cell_size
            outer_radius = inner_radius + cell_size
            theta_ccw = cell.column * theta
            theta_cw = theta_ccw + theta
            theta_center = theta_ccw + (theta / 2)
            theta_z = theta_cw + (theta / 2)
            theta_w = theta_center - theta / 4
            theta_y = theta_center + theta / 4

# The four corners of a cell are abcd
# 
#   center
#      v
#    c   a
#  z  yxw
#    d   b

            a_coord = polarToRect(center, inner_radius, theta_ccw)
            c_coord = polarToRect(center, inner_radius, theta_cw)
            d_coord = polarToRect(center, outer_radius, theta_cw)
            v_coord = polarToRect(center, center_radius_inner, theta_center)
            w_coord = polarToRect(center, center_radius, theta_w)
            x_coord = polarToRect(center, center_radius, theta_center)
            y_coord = polarToRect(center, center_radius, theta_y)
            z_coord = polarToRect(center, center_radius, theta_z)

            if not cell.linked(cell.inward):
                addArc(dwg, (c_coord.x, c_coord.y), (a_coord.x, a_coord.y), inner_radius, 'black')
            if cell.linked(cell.inward):
                dwg.add(dwg.line((v_coord.x, v_coord.y), (x_coord.x, x_coord.y), stroke="red"))
            if not cell.linked(cell.cw):
                dwg.add(dwg.line((c_coord.x, c_coord.y), (d_coord.x, d_coord.y), stroke=svgwrite.rgb(10, 10, 16, '%')))
            if cell.linked(cell.cw):
                addArc(dwg, (z_coord.x, z_coord.y), (x_coord.x, x_coord.y), center_radius, 'red')
            if len(cell.outward) == 2:
                if cell.outward[0].linked(cell):
                    addArc(dwg, (x_coord.x, x_coord.y), (w_coord.x, w_coord.y), center_radius, 'red')
                if cell.outward[1].linked(cell):
                    addArc(dwg, (y_coord.x, y_coord.y), (x_coord.x, x_coord.y), center_radius, 'red')

        dwg.add(dwg.circle(center=(center, center), r=(self.rows * cell_size), stroke=svgwrite.rgb(10, 10, 16, '%'), fill='none'))
        dwg.save()


    def to_svg_contour(self, cell_size = 10, with_distance = False):

        img_size = 2 * self.rows * cell_size
        margin = 10
        center = img_size / 2 + margin
        insert = ("", "_distances")[with_distance]
        if with_distance:
            dwg = svgwrite.Drawing('./exports/polarmaze_distance.svg')
        else:
            dwg = svgwrite.Drawing('./exports/polarmaze.svg')

        for cell in self.each_cell():
            if cell.row == 0: continue

            theta = 2 * math.pi / len(self.grid[cell.row])

            inner_radius = cell.row * cell_size
            center_radius = inner_radius + cell_size / 2
            outer_radius = inner_radius + cell_size

            theta_ccw = cell.column * theta
            theta_q = theta_ccw + theta / 4
            theta_center = theta_ccw + (theta / 2)
            theta_s = theta_ccw + (3 * theta / 4)
            theta_cw = theta_ccw + theta

# The polar cell points
# o - origin
# abcd - edges
# vw -      
#
#    + a +
#    dsoqc
#    +tbr+
#

            a_coord = polarToRect(center, inner_radius, theta_center)
            o_coord = polarToRect(center, center_radius, theta_center)
            b_coord = polarToRect(center, outer_radius, theta_center)

            c_coord = polarToRect(center, center_radius, theta_ccw)
            d_coord = polarToRect(center, center_radius, theta_cw)

            q_coord = polarToRect(center, center_radius, theta_q)
            r_coord = polarToRect(center, outer_radius, theta_q)
            s_coord = polarToRect(center, center_radius, theta_s)
            t_coord = polarToRect(center, outer_radius, theta_s)

            if with_distance:
                percent = (cell.distance % 200) / 2
                color = svgwrite.rgb(percent, 10, 10, '%')
                if cell.distance % 600 > 200:
                    color = svgwrite.rgb(10, percent, 10, '%')
                if cell.distance % 600 > 400:
                    color = svgwrite.rgb(10, 10, percent, '%')
                dwg.add(dwg.text(cell.distance, insert=(o_coord.x, o_coord.y), font_size='5px', fill=color ))
                
            if has_corner(cell):
                if cell.linked(cell.inward) and cell.linked(cell.ccw):
                    addArc(dwg, (a_coord.x, a_coord.y), (c_coord.x, c_coord.y), cell_size / 1.4, 'black')
                if len(cell.outward) == 1 and cell.linked(cell.outward[0]) and cell.linked(cell.ccw):
                    addArc(dwg, (c_coord.x, c_coord.y), (b_coord.x, b_coord.y), cell_size / 1.4, 'black')
                if cell.linked(cell.inward) and cell.linked(cell.cw):
                    addArc(dwg, (d_coord.x, d_coord.y), (a_coord.x, a_coord.y), cell_size / 1.4, 'black')
                if len(cell.outward) == 1 and cell.linked(cell.outward[0]) and cell.linked(cell.cw):
                    addArc(dwg, (b_coord.x, b_coord.y), (d_coord.x, d_coord.y), cell_size / 1.4, 'black')
            else:
                if cell.linked(cell.inward):
                    if cell.distance == 1: 
                        dwg.add(dwg.line((o_coord.x, o_coord.y), (center, center), stroke="black"))
                    else:
                        dwg.add(dwg.line((o_coord.x, o_coord.y), (a_coord.x, a_coord.y), stroke="black"))
                if cell.linked(cell.cw):
                    addArc(dwg, (d_coord.x, d_coord.y), (o_coord.x, o_coord.y), center_radius, 'black')
                if cell.linked(cell.ccw):
                    addArc(dwg, (o_coord.x, o_coord.y), (c_coord.x, c_coord.y), center_radius, 'black')
                if len(cell.outward) == 1:
                    if cell.outward[0].linked(cell):
                        dwg.add(dwg.line((o_coord.x, o_coord.y), (b_coord.x, b_coord.y), stroke="black"))
                if len(cell.outward) == 2:
                    if cell.outward[0].linked(cell):
                        addArc(dwg, (o_coord.x, o_coord.y), (q_coord.x, q_coord.y), center_radius, 'black')
                        dwg.add(dwg.line((q_coord.x, q_coord.y), (r_coord.x, r_coord.y), stroke="black"))
                    if cell.outward[1].linked(cell):
                        addArc(dwg, (s_coord.x, s_coord.y), (o_coord.x, o_coord.y), center_radius, 'black')
                        dwg.add(dwg.line((s_coord.x, s_coord.y), (t_coord.x, t_coord.y), stroke="black"))


        # dwg.add(dwg.circle(center=(center, center), r=(self.rows * cell_size), stroke=svgwrite.rgb(10, 10, 16, '%'), fill='none'))
        dwg.save()

def addArc(dwg, p0, p1, radius, color):
    """ Adds an arc that bulges to the right as it moves from p0 to p1 """
    # https://stackoverflow.com/questions/25019441/arc-pie-cut-in-svgwrite
    args = {'x0':p0[0], 
        'y0':p0[1], 
        'xradius':radius, 
        'yradius':radius, 
        'ellipseRotation':0, #has no effect for circles
        'x1':(p1[0]-p0[0]), 
        'y1':(p1[1]-p0[1])}
    dwg.add(dwg.path(d="M %(x0)f,%(y0)f a %(xradius)f,%(yradius)f %(ellipseRotation)f 0,0 %(x1)f,%(y1)f"%args,
        fill="none", 
        stroke=color, stroke_width=1
    ))

def polarToRect(center, r, angle):
    result = Point(center + r * math.cos(angle), center + r * math.sin(angle))
    return result

def showCell(dwg, grid, cell, cell_size, center):
    radius = (cell.row + .5) * cell_size
    theta = 2 * math.pi / len(grid[cell.row])
    angle = (cell.column + .5) * theta
    coords = polarToRect(center, radius, angle)
    dwg.add(dwg.circle(center=(coords.x, coords.y), r=(cell_size * .25), stroke=svgwrite.rgb(10, 10, 16, '%'), fill='red'))

def has_corner(cell):
    if len(cell.get_links()) != 2:
        return False
    if len(cell.outward) == 2:
        return False
    if cell.linked(cell.inward) and len(cell.outward) == 1 and cell.linked(cell.outward[0]):
        return False
    if cell.linked(cell.ccw) and cell.linked(cell.cw):
        return False
    return True
