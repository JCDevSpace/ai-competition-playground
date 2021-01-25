import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../.."))

from tkinter import *
from Common.View.board_artist import BoardArtist
from Common.View.penguin_artist import PenguinArtist
from Common.View.score_board_artist import ScoreBoardArtist

# A Style is a Map(String, (Int or String)) which maps different stylistic constants to their values.

TILE_SIZE = 50

DEFAULT_STYLE = {
    "tile_size": TILE_SIZE,
    "penguin_width": int(TILE_SIZE * 0.8),
    "fish_height": int(TILE_SIZE * 0.2),
    "fish_width": int(TILE_SIZE * 1.4),
    "fish_space": int(TILE_SIZE * .1),
    "outline_width": max(1, int(TILE_SIZE * .02)),
    "scoreboard_width": TILE_SIZE * 4,
    "scoreboard_outline": "black",
    "scoreboard_fill": "light grey",
    "font_size": 12,
    "text_offset": TILE_SIZE,
    "line_spacing": 3,
    "fill_color": "orange",
    "outline_color": "red",
    "penguin_outline": "black",
    "fish_outline": "black",
    "fish_color": "blue",
    "bg_color": "sky blue"
}


# A FishView is responsible for rendering a GameState and the rest of the GUI needed (in the future)
class FishView:

    # Given an GameState and a Style creates a FishView and renders it
    # GameState, Style -> FishView
    def __init__(self, row, col, style=DEFAULT_STYLE):
        #self.update_game_state(initial_game_state)
        self.style = style

        self.frame = Tk()
        self.width = col
        self.height = row
        self.canvas = Canvas(self.frame, bg=self.style['bg_color'], width=self.calculate_frame_width(), height=self.calculate_frame_height())


    # Saves the different pieces of the gamestate into the FishView object
    # GameState -> Void
    def update_game_state(self, game_state):
        self.board_state = game_state[0]
        self.player_data = game_state[1]
        self.penguin_locations = game_state[2]
        self.turn = game_state[3]
        self.scores = game_state[4]
        self.render()

    # Returns the height that the frame (window) should have given the size of the board
    # Void -> Int
    def calculate_frame_height(self):
        return (self.height * self.style['tile_size']) + self.style['tile_size']

    # Returns the width that the frame (window) should have given the size of the board
    # Void -> Int
    def calculate_frame_width(self):
        return (self.width * self.style['tile_size'] * 4) + self.style['tile_size'] + self.style['scoreboard_width']

    # Finds the union of all penguin locaitons
    # Void -> List[Position]
    def all_penguin_locations(self):
        occupied_tiles = []
        for positions in self.penguin_locations.values():
            occupied_tiles += positions
        return occupied_tiles

    # Clears the previous rendering of the game state and rerenders it
    # Void -> Void
    def render(self):
        self.canvas.delete("all")

        BoardArtist(self.board_state, self.all_penguin_locations(), self.style).draw(self.canvas)
        for color, positions in self.penguin_locations.items():
            for position in positions:
                PenguinArtist(color, position, self.style).draw(self.canvas)

        ScoreBoardArtist(self.calculate_frame_width() - self.style['scoreboard_width'],
            self.calculate_frame_height(),
            self.player_data, self.scores,
            self.turn, self.style).draw(self.canvas)

        self.canvas.pack()
        self.frame.update_idletasks()
        self.frame.update()
