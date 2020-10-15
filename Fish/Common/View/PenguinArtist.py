from View.Artist import Artist


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
        x, y = self.get_tile_center(self.get_x_offset(self.row, self.col), self.get_y_offset(self.row))
        r = self.style["penguin_width"]
        canvas.create_oval(x - r, y - r, x + r, y + r, outline=self.style["penguin_outline"], fill=self.color,
                           width=self.style["outline_width"])
