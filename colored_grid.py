from grid import Grid

class ColoredGrid(Grid):

    def __init__(self, rows, columns):
        self.rows, self.columns = rows, columns
        self.grid = self.prepare_grid()
        self.configure_cells()
        self.distances = {}
        self.maximum = 0;

    def background_color_for(self, cell):
        if self.distances.get(cell) is None:
            return None
        distance = self.distances.get(cell)
        intensity = (self.maximum - int(distance)) / self.maximum
        dark = int(255 * intensity)
        bright = 128 + int(127 * intensity)

        hex_string = hex(dark * 256 * 256 + bright * 256 + dark)[2:]
        if len(hex_string) == 4:
            hex_string = "00" + hex_string
        elif len(hex_string) == 5:
            hex_string = "0" + hex_string
        return "#" + hex_string
