from tkinter import *
import math

from View.Artist import Artist
from View.TileArtist import TileArtist

# A BoardArtist is responsible for drawing the board.
class BoardArtist(Artist):
    def __init__(self, game_state, style):
        super(style)
        self.game_state = game_state

    def draw(self, canvas):
        for row in range(0, len(self.game_state[0])):
            for col in range(0, len(self.game_state[row])):
                x_offset = calculate_x_offset(row, col)
                y_offset = calculate_y_offset(row)
                tile = TileArtist(x_offset, y_offset, game_state[row][col], self.style)
                tile.draw(canvas)

if __name__ == '__main__':
    BoardArtist([[1, "red", "brown"], [1, 2, 3], [4, -1, 5]])
    mainloop()
