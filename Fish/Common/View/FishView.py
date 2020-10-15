from tkinter import *

from View.BoardArtist import BoardArtist
from View.PenguinArtist import PenguinArtist

# A Style is a Map(String, (Int or String)) which maps different stylistic constants to their values.

TILE_SIZE = 100

DEFAULT_STYLE = {
    "tile_size": TILE_SIZE,
    "penguin_width": int(TILE_SIZE * 0.8),
    "fish_height": int(TILE_SIZE * 0.2),
    "fish_width": int(TILE_SIZE * 1.4),
    "fish_space": int(TILE_SIZE * .1),
    "outline_width": max(1, int(TILE_SIZE * .02)),
    "fill_color": "orange",
    "outline_color": "red",
    "penguin_outline": "black",
    "fish_outline": "black",
    "fish_color": "blue",
    "bg_color": "white"
}


# A FishView is responsible for rendering a GameState and the rest of the GUI needed (in the future)
class FishView:

    # Given an GameState and a Style creates a FishView and renders it
    # GameState, Style -> FishView
    def __init__(self, initial_game_state, style=DEFAULT_STYLE):
        self.update_game_state(initial_game_state)
        self.style = style

        self.frame = Tk()
        self.width = len(self.board_state[0])
        self.height = len(self.board_state)
        self.canvas = Canvas(self.frame, bg=self.style['bg_color'], width=self.calculate_frame_width(),
                             height=self.calculate_frame_height())

        self.render()

    # Saves the different pieces of the gamestate into the FishView object
    # GameState -> Void
    def update_game_state(self, game_state):
        self.board_state = game_state[0]
        self.player_data = game_state[1]
        self.penguin_locations = game_state[2]
        self.turn = game_state[3]

    # Returns the height that the frame (window) should have given the size of the board
    # Void -> Int
    def calculate_frame_height(self):
        return (self.height * self.style['tile_size']) + self.style['tile_size']

    # Returns the width that the frame (window) should have given the size of the board
    # Void -> Int
    def calculate_frame_width(self):
        return (self.width * self.style['tile_size'] * 4) + self.style['tile_size']

    # Draws the FishView in a new window inlcuding the penguins and the board
    # Void -> Void
    def render(self):
        BoardArtist(self.board_state, self.style).draw(self.canvas)
        for color, positions in self.penguin_locations.items():
            for position in positions:
                PenguinArtist(color, position, self.style).draw(self.canvas)

        self.canvas.pack()
