from tkinter import *
import math
from View.TileView import TileView

class BoardView:
    BG_COLOR = "white"

    def __init__(self, initial_board_state):
        self.frame = Tk()

        self.width = len(initial_board_state[0])
        self.height = len(initial_board_state)

        self.canvas = Canvas(self.frame, bg=self.BG_COLOR, width=self.calculate_frame_width(), height=self.calculate_frame_height())

        self.draw_game_state(initial_board_state)

    def calculate_frame_height(self):
        return (self.height * TileView.TILE_SIZE) + TileView.TILE_SIZE

    def calculate_frame_width(self):
        return (self.width * TileView.TILE_SIZE * 4) + TileView.TILE_SIZE

    def draw_game_state(self, game_state):
        for row in range(0, len(game_state)):
            for col in range(0, len(game_state[row])):
                tile = TileView(row, col, game_state[row][col])
                tile.draw(self.canvas)

        self.canvas.pack()

if __name__ == '__main__':
    BoardView([[1, "red", "brown"], [1, 2, 3], [4, -1, 5]])
    mainloop()
