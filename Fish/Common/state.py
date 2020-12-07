# A GameState is a (Board, List[Color], {Color, List[Position]}, Int, {Color, Int})
# The GameState object represents all the data need to run the fish game.
# The Board keeps track of the tiles and number of fish on those tiles,
# the List[Color] keeps information about the players in the game_state,
# and the {Color, List[Position]} keeps track of where the players penguins
# are on the board. The Int represents the index of the player whose turn it is.
# Finally, the {Color, Int} represents each players current score.

# Color is  one of "red", "white", "brown", "black"

# A Position is a (Int, Int)
# It represents a location on the board, the first element being the rows
# and the second element being the column.

import copy
import sys

sys.path.append('..')
sys.path.append('../..')

from Fish.Common.board import Board

class GameState:

    # Creates an initial GameState given the Colors playing and a Board.
    # Optional to include penguin positions, turn, and scores to construct intermediate states.
    # The order of colors in which the game state is constructed with represents the order of
    # the turns
    # Board, List[Color] ?{Color, List[Position]}, ?Int, ?{Color, Int} -> GameState
    def __init__(self, board, colors, penguin_positions=None, turn=None, scores=None):
        self.colors = colors
        self.board = board

        if not penguin_positions:
            self.penguin_positions = {}
            for color in self.colors:
                self.penguin_positions[color] = []
        else:
            self.penguin_positions = penguin_positions

        if not scores:
            self.scores = {}
            for color in self.colors:
                self.scores[color] = 0
        else:
            self.scores = scores

        if not turn:
            self.turn = 0
        else:
            self.turn = turn

    # Creates a deep copy of this GameState
    # Void -> GameState
    def deepcopy(self):
        board = self.board.deepcopy()
        colors = copy.deepcopy(self.colors)
        penguin_positions = copy.deepcopy(self.penguin_positions)
        turn = self.turn
        scores = copy.deepcopy(self.scores)

        return GameState(board, colors, penguin_positions=penguin_positions, turn=turn, scores=scores)

    # Returns a GameState object from the tuple data
    # Serialized GameState -> GameState
    def generate_game_state(layout, players, penguin_positions, turn, scores):
        board = Board(None, None, layout=layout)
        players = copy.deepcopy(players)
        penguin_positions = copy.deepcopy(penguin_positions)
        scores = copy.deepcopy(scores)

        return GameState(board, players, penguin_positions, turn, scores)

    # Returns the color of the player who's turn it is currently
    # Void -> Color
    def get_current_color(self):
        return self.colors[self.turn]

    # Adds a penguin for a particular player at a Position
    # Modifies self.board, and self.penguin_positions
    # The optional int tells this method to insert the penguin in a certain
    # index of penguin positions, this is used to maintain the order of players 
    # penguins to accomodate the test harness
    # Color, Position, ?Int -> Void
    # raises ValueError if trying to place a penguin at a non-open Position (has penguin there already or is a hole)
    def place_penguin(self, color, posn, index=None):
        if self.get_current_color() != color:
            raise ValueError("not the current players turn")

        if self.placable_position(posn):
            if index is not None:
                self.penguin_positions[color].insert(index, posn)
            else:
                self.penguin_positions[color].append(posn)

            # update the turn counter
            self.increment_turn()
        else:
            raise ValueError("placing penguin on invalid tile")

    # Attempts to Move a player's penguin from the start Position to the End Position
    # Modifies self.board and self.penguin_positions
    # Color, Position, Position -> Void
    # raises ValueError if there is no penguin for that player at the start Position or
    #   if the end position is not a valid move from the start Position
    def move_penguin(self, color, start_posn, end_posn):
        if self.get_current_color() != color:
            raise ValueError("not the current players turn")

        if start_posn in self.penguin_positions[color] and end_posn in self.board.get_valid_moves(start_posn, self.get_occupied_tiles()):
            # remove the tile from the board and add
            # the number of fish to this players score
            self.scores[color] += self.board.get_tile(start_posn)
            self.board.add_hole(start_posn)

            # update this players penguin positions while maintaining the
            # order of the list
            index = self.penguin_positions[color].index(start_posn)
            del self.penguin_positions[color][index]
            self.place_penguin(color, end_posn, index)

        else:
            raise ValueError("invalid move")

    # Applies a Move to the game state
    # Move -> Void
    # raises value error if the player attempting to move is not the current player
    def apply_move(self, move):
        if move[0] != self.get_current_color():
            raise ValueError("a player is attempting to move when it is no their turn")

        # len(move) == 2 and
        if not move[1]:
            # skip the players turn for this type of move
            self.increment_turn()
        elif len(move) == 3:
            self.move_penguin(*move)
        else:
            raise ValueError("Invalid Move")


    # Increments the turn counter of the game state. Wraps around to 0 after the
    # last person moves.
    # Void -> Void
    def increment_turn(self):
        self.turn = (self.turn + 1) % len(self.colors)

    # Returns whether or not the game is over, meaning no one can move.
    # Void -> Boolean
    def game_over(self):
        for color in self.colors:
            if self.has_moves_left(color):
                return False
        return True

    # Returns whether or not a specific player has any available moves
    # Color -> Boolean
    def has_moves_left(self, color):
        for posn in self.penguin_positions[color]:
            if len(self.board.get_valid_moves(posn, self.get_occupied_tiles())) > 0:
                return True
        return False

    # Returns a set of all the occupied tiles on the board
    # Void -> Set(Positon)
    def get_occupied_tiles(self):
        occupied_tiles = []
        for positions in self.penguin_positions.values():
            occupied_tiles += positions
        return occupied_tiles

    # Returns true if a penguin can be placed on a position
    # Position -> Boolean
    def placable_position(self, position):
        return self.board.is_open(position, self.get_occupied_tiles())

    # Returns the list of Moves available to the current player.
    # Void -> List[Move]
    def get_current_player_valid_moves(self):
        player = self.get_current_color()
        player_moves = []

        if self.has_moves_left(player):
            for start_pos in self.penguin_positions[player]:
                end_positions = self.board.get_valid_moves(start_pos, self.get_occupied_tiles())
                for end_pos in end_positions:
                    player_moves.append((player, start_pos, end_pos))
        elif not self.game_over():
            player_moves = [(player, False, False)]

        return player_moves

    # Removes the given Player from the game
    # Color -> Void
    def remove_player(self, color):
        del self.penguin_positions[color]
        del self.scores[color]

        # Update the turn counter when removing a color from
        # the list of colors
        index = self.colors.index(color)
        if index < self.turn:
            self.turn -= 1

        self.colors.remove(color)
        if len(self.colors) == 0:
            return

        self.turn %= len(self.colors)

    # Returns the a list of players who are tied for the most points
    # Void -> List[Player]
    def get_winners(self):
        max_score = max(self.scores.values())
        return [key for key, value in self.scores.items() if value == max_score]

    # Returns a copy of the GameState as the atomic data defined at the top of the file.
    # Void -> Serialized GameState
    def get_game_state(self):
        players = copy.copy(self.colors)
        penguin_positions = {player: positions for player, positions in self.penguin_positions.items()}
        player_scores = {player: score for player, score in self.scores.items()}

        return (self.board.get_board_state(), players, penguin_positions, self.turn, player_scores)

    def get_score(self, color):
        return self.scores[color]
