from Common.View.Artist import Artist

# A Style is a Map(String, (Int or String)) which maps different stylistic constants to their values.

# A TileArtist is responsible for drawing an individual tile.
class TileArtist(Artist):

    # Generates a Tile artist given the offsets and what type of tile to draw
    # Int, Int, Tile, Boolean, Style -> TileArtist
    def __init__(self, x_offset, y_offset, tile_data, draw_fish, style):
        super().__init__(style)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.tile_data = tile_data
        self.draw_fish = draw_fish

    # Returns the list of points each pair of these is a vertex of the hexagon.
    # This would be better as a List[Position] but the create_polygon method from tkinter takes it in in this form.
    # Void -> List[Int]
    def get_tile_outline(self):
        size = self.style["tile_size"]
        x_offset = self.x_offset
        y_offset = self.y_offset

        return [
            size + x_offset, y_offset,
            2 * size + x_offset, y_offset,
            3 * size + x_offset, size + y_offset,
            2 * size + x_offset, 2 * size + y_offset,
            size + x_offset, 2 * size + y_offset,
            x_offset, size + y_offset
        ]

    # Draws the tile from the colors chosen in the style.
    # Canvas -> Void
    def draw_tile(self, canvas):
        canvas.create_polygon(self.get_tile_outline(), outline=self.style["outline_color"],
                              fill=self.style["fill_color"], width=self.style["outline_width"])

    # Draws the fish onto the canvas depending on how many are supposed to be on the tile
    # Canvas -> Void
    def draw_fish(self, canvas):
        x, y = self.get_tile_center(self.x_offset, self.y_offset)
        x_offset = x - (self.style["fish_width"] // 2)
        y_start = y - int((self.tile_data / 2) * self.style["fish_height"]) - int(
            ((self.tile_data - 1) / 2) * self.style["fish_space"])
        for fish in range(0, self.tile_data):
            y_offset = y_start + (fish * (self.style["fish_height"] + self.style["fish_space"]))
            canvas.create_rectangle(x_offset, y_offset,
                                    x_offset + self.style["fish_width"],
                                    y_offset + self.style["fish_height"],
                                    outline=self.style["fish_outline"],
                                    fill=self.style["fish_color"],
                                    width=self.style["outline_width"])

    # Draws the Tile including the fish onto the canvas.
    # Canvas -> Void
    def draw(self, canvas):
        if self.tile_data == 0:
            return
        elif self.tile_data in range(0, 6):
            self.draw_tile(canvas)
            if self.draw_fish:
              self.draw_fish(canvas)
