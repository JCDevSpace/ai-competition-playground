import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../.."))

from Fish.Common.View.fish_view import FishView
from Fish.Common.state import GameState

# A GameVisualizer is a component that visualizes the progress of games
# by showing a simple GUI where the board along with every player's avatars
# and score can be seen. It acts as an observer to any game of fish and can
# be added to a list of observers to a game and be notified by the referee
# when the game state changes.

class GameVisualizer:

    # Construct an instance of the game visualizer
    def __init__(self):
        self.game_state = None
        self.visualizer = None

    # Updates the observer of the initial state of the game
    # GameState -> Void
    def inital_state_update(self, game_state):
        self.game_state = GameState.generate_game_state(*game_state)

        board = game_state[0]        
        self.visualizer = FishView(len(board), len(board[0]))

    # Updates the observer of a placement action in the game
    # Placement -> Void
    def placement_update(self, placement):
        self.game_state.place_penguin(*placement)
        self.redraw()

    # Updates the observer of a movement action in the game
    # Movement -> Void
    def movement_update(self, move):
        self.game_state.apply_move(move)
        self.redraw()

    # Updates the observer of a player kick in the game
    # Kick -> Void
    def player_kick_update(self, kick):
        self.game_state.remove_player(kick[0])
        self.redraw()

    # Redraws the GUI for the updated game state
    def redraw(self):
        self.visualizer.update_game_state(self.game_state.get_game_state())
        self.visualizer.render()