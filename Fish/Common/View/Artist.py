

class Artist:
    def __init__(self, style):
      self.style = style

    def get_tile_center(self, x_offset, y_offset):
        return x_offset + int(1.5 * self.style["tile_size"]), y_offset + self.style["tile_size"]

    def calculate_y_offset(self, row):
        return self.style["tile_size"] * row

    def calculate_x_offset(self, row, col):
        if row % 2 == 0:
            return self.style["tile_size"] * 4 * col
        else:
            return (self.style["tile_size"] * 4 * col) + (2 * self.style["tile_size"])

    # to be implemented by child classes
    def draw(self, canvas):
        pass
