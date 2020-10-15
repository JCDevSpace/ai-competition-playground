# A Style is a Map(String, (Int or String)) which maps different stylistic constants to their values.


# An Artist is an "Abstract" class for something which can draw something.
# Abstract classes dont exist in vanilla python (can import it from abc but didnt see it as necessary)
class Artist:
    #Creates an absract Artist given a style.
    # Style -> Artist
    def __init__(self, style):
      self.style = style

    # Returns the center of a tile given the x and y offsets for the top left of the tile
    # Int, Int -> Position
    def get_tile_center(self, x_offset, y_offset):
        return x_offset + int(1.5 * self.style["tile_size"]), y_offset + self.style["tile_size"]

    # Returns the y offset of tile given the row where it is from
    # Int -> Int
    def calculate_y_offset(self, row):
        return self.style["tile_size"] * row

    # Returns the x offset of a tile given the row and column where it is from
    # Int, Int -> Int
    def calculate_x_offset(self, row, col):
        if row % 2 == 0:
            return self.style["tile_size"] * 4 * col
        else:
            return (self.style["tile_size"] * 4 * col) + (2 * self.style["tile_size"])

    # Draws the Artist's specialty on the canvas.
    # This is an 'abstract' method to be implemented by child's classes
    def draw(self, canvas):
        pass
