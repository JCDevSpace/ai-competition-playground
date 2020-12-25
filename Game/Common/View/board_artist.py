import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../.."))

from Common.View.artist import Artist
from Common.View.tile_artist import TileArtist

# A Style is a Map(String, (Int or String)) which maps different stylistic constants to their values.

# A BoardArtist is responsible for drawing the board.
class BoardArtist(Artist):
    # Creates a BoardArtist given the board_state to draw and the style to follow
    # List[List[Tile]], List[Position], Style -> BoardArtist
    def __init__(self, board_state, occupied_tiles, style):
        super().__init__(style)
        self.board_state = board_state
        self.occupied_tiles = occupied_tiles

    # Draws the board onto the canvas
    # Canvas -> Void
    def draw(self, canvas):
        for row in range(0, len(self.board_state)):
            for col in range(0, len(self.board_state[row])):
                x_offset = self.calculate_x_offset(row, col)
                y_offset = self.calculate_y_offset(row)
                draw_fish = (row, col) not in self.occupied_tiles
                tile = TileArtist(x_offset, y_offset, self.board_state[row][col], draw_fish, self.style)
                tile.draw(canvas)

# if __name__ == '__main__':
#     BoardArtist([[1, 0, 0], [1, 2, 3], [4, -1, 5]])
#     mainloop()
