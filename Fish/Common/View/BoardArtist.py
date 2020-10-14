from tkinter import *
import math

from View.Artist import Artist
from View.TileArtist import TileArtist

# A BoardArtist is responsible for drawing the board.
class BoardArtist(Artist):
    def __init__(self, board_state, style):
        super().__init__(style)
        self.board_state = board_state

    def draw(self, canvas):
        for row in range(0, len(self.board_state)):
            for col in range(0, len(self.board_state[row])):
                x_offset = self.calculate_x_offset(row, col)
                y_offset = self.calculate_y_offset(row)
                tile = TileArtist(x_offset, y_offset, self.board_state[row][col], self.style)
                tile.draw(canvas)

# if __name__ == '__main__':
#     BoardArtist([[1, 0, 0], [1, 2, 3], [4, -1, 5]])
#     mainloop()
