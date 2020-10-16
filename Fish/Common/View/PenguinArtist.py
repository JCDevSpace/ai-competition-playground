from Common.View.Artist import Artist

# A Style is a Map(String, (Int or String)) which maps different stylistic constants to their values.

# A PenguinArtist is responsible for drawing a penguin on the board.
class PenguinArtist(Artist):

    # Creates a PenguinArtist given the color of the penguin and where on the board it sits
    # Color, Position, Style -> PenguinArtist
    def __init__(self, color, position, style):
        super().__init__(style)
        self.row = position[0]
        self.col = position[1]
        self.color = color

    # Draws the penguin at the position needed on the Canvas.
    # Canvas -> Void
    def draw(self, canvas):
        x, y = self.get_tile_center(self.calculate_x_offset(self.row, self.col), self.calculate_y_offset(self.row))
        r = self.style["penguin_width"]
        canvas.create_oval(x - r, y - r, x + r, y + r, outline=self.style["penguin_outline"], fill=self.color,
                           width=self.style["outline_width"])
