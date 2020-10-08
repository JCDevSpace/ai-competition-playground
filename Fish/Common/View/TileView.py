from tkinter import *

class TileView:
    TILE_SIZE = 100
    FILL_COLOR = "orange"
    OUTLINE_COLOR = "red"
    OUTLINE_WIDTH = 2
    PENGUIN_WIDTH = 80
    PENGUIN_OUTLINE = "black"
    FISH_WIDTH = 140
    FISH_HEIGHT = 20
    FISH_SPACE = 10
    FISH_OUTLINE = "black"
    FISH_COLOR = "blue"

    def __init__(self, row, col, tile_data):
        self.row = row
        self.col = col
        self.tile_data = tile_data

    def get_y_offset(self):
        return self.TILE_SIZE * self.row

    def get_x_offset(self):
        if self.row % 2 == 0:
            return self.TILE_SIZE * 4 * self.col
        else:
            return (self.TILE_SIZE * 4 * self.col) + (2 * self.TILE_SIZE)

    def get_tile_outline(self):
        size = self.TILE_SIZE
        x_offset = self.get_x_offset()
        y_offset = self.get_y_offset()

        return [
            size + x_offset, y_offset,
            2 * size + x_offset, y_offset,
            3 * size + x_offset, size + y_offset,
            2 * size + x_offset, 2 * size + y_offset,
            size + x_offset, 2 * size + y_offset,
            x_offset, size + y_offset
        ]

    def get_tile_center(self):
        return self.get_x_offset() + int(1.5 * self.TILE_SIZE), self.get_y_offset() + self.TILE_SIZE

    def draw_tile(self, canvas):
        canvas.create_polygon(self.get_tile_outline(), outline=self.OUTLINE_COLOR, fill=self.FILL_COLOR, width=self.OUTLINE_WIDTH)

    def draw_penguin(self, canvas):
        x, y = self.get_tile_center()
        r =  self.PENGUIN_WIDTH
        canvas.create_oval(x - r, y - r, x + r, y + r, outline=self.PENGUIN_OUTLINE, fill=self.tile_data, width=self.OUTLINE_WIDTH)

    def draw_fish(self, canvas):
        x, y = self.get_tile_center()
        x_offset = x - (self.FISH_WIDTH // 2)
        y_start = y - int((self.tile_data / 2) * self.FISH_HEIGHT) - int(((self.tile_data - 1) / 2) * self.FISH_SPACE)
        for fish in range(0, self.tile_data):
            y_offset = y_start + (fish * (self.FISH_HEIGHT + self.FISH_SPACE))
            canvas.create_rectangle(x_offset, y_offset, x_offset + self.FISH_WIDTH, y_offset + self.FISH_HEIGHT, outline=self.FISH_OUTLINE, fill=self.FISH_COLOR, width=self.OUTLINE_WIDTH)

    def draw(self, canvas):
        if self.tile_data == -1:
            return
        elif self.tile_data in range(1, 6):
            self.draw_tile(canvas)
            self.draw_fish(canvas)
        else:
            self.draw_tile(canvas)
            self.draw_penguin(canvas)
