from tkinter import *
from View.Artist import Artist

# A TileArtist is responsible for drawing an individual tile.
class TileArtist(Artist):
    def __init__(self, x_offset, y_offset, tile_data, style):
        super(style)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.tile_data = tile_data

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

    def draw_tile(self, canvas):
        canvas.create_polygon(self.get_tile_outline(), outline=self.style["outline_color"], fill=self.style["fill_color"], width=self.style["outline_width"])

    def draw_fish(self, canvas):
        x, y = self.get_tile_center(self.x_offset, self.y_offset)
        x_offset = x - (self.style["fish_width"] // 2)
        y_start = y - int((self.tile_data / 2) * self.style["fish_height"]) - int(((self.tile_data - 1) / 2) * self.style["fish_space"])
        for fish in range(0, self.tile_data):
            y_offset = y_start + (fish * (self.style["fish_height"] + self.style["fish_space"]))
            canvas.create_rectangle(x_offset, y_offset, x_offset + self.style["fish_width"], y_offset + self.style["fish_height"], outline=self.style["fish_outline"], fill=self.self.style["fish_color"], width=self.style["outline_width"])

    def draw(self, canvas):
        if self.tile_data == -1:
            return
        elif self.tile_data in range(0, 6):
            self.draw_tile(canvas)
            self.draw_fish(canvas)
