# A GameState is a (Board, List[Player], {Player, List[Position]}, Int, {Player, Int})
# The GameState object represents all the data need to run the fish game.
# The Board keeps track of the tiles and number of fish on those tiles,
# the List[Player] keeps information about the players in the game_state,
# and the {Player, List[Position]} keeps track of where the players penguins
# are on the board. The Int represents the index of the player whose turn it is.
# Finally, the {Player, Int} represents each players current score.

# A Player is a (Color, Int)
# This represents the the data for a player. The Color is the
# penguin color that they have been assigned and the Int is their age.

# Color is  one of "red", "white", "brown", "black"

# A Position is a (Int, Int)
# It represents a location on the board, the first element being the rows
# and the second element being the column.

import copy

from Common.board import Board
from Common.Model.Player import Player

class GameState:

    # Creates an initial GameState given the Players playing and a Board.
    # Optional to include penguin positions, turn, and scores to construct intermediate states.
    # This also sorts the players by their age, ensuring that the players list
    # in the state is the order in which they would play.
    # List[Player], Board, ?{Player, List[Position]}, ?Int, ?{Player, Int} -> GameState
    def __init__(self, players, board, penguin_positions=None, turn=None, scores=None):
        self.players = sorted(players, key=(lambda x: x.get_age()))
        self.board = board

        if not penguin_positions:
            self.penguin_positions = {}
            for player in self.players:
                self.penguin_positions[player] = []
        else:
            self.penguin_positions = penguin_positions

        if not scores:
            self.scores = {}
            for player in self.players:
                self.scores[player] = 0
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
        players = copy.deepcopy(self.players)
        penguin_positions = copy.deepcopy(self.penguin_positions)
        turn = self.turn
        scores = copy.deepcopy(self.scores)

        return GameState(players, board, penguin_positions=penguin_positions, turn=turn, scores=scores)

    # Returns a GameState object from the tuple data
    # GameState -> GameState
    def generate_game_state(layout, players, penguin_positions, turn, scores):
        board = Board(None, None, layout=layout)
        players = [Player(*player) for player in players]
        colors = {player.get_color(): player for player in players}
        penguin_positions = {colors[color]: positions for color, positions in penguin_positions.items()}
        scores = {colors[color]: score for color, score in scores.items()}

        return GameState(players, board, penguin_positions, turn, scores)

    # Returns the player who's turn it is currently
    # Void -> Player
    def get_current_player(self):
        return self.players[self.turn]

    # Adds a penguin for a particular player at a Position
    # Modifies self.board, and self.penguin_positions
    # Player, Position -> Void
    # raises ValueError if trying to place a penguin at a non-open Position (has penguin there already or is a hole)
    def place_penguin(self, player, posn, index=None):
        if self.get_current_player() != player:
            raise ValueError("not the current players turn")

        if self.placable_position(posn):
            if index is not None:
                self.penguin_positions[player].insert(index, posn)
            else:
                self.penguin_positions[player].append(posn)

            # update the turn counter
            self.increment_turn()
        else:
            raise ValueError("placing penguin on invalid tile")

    # Attempts to Move a player's penguin from the start Position to the End Position
    # Modifies self.board and self.penguin_positions
    # Player, Position, Position  -> Void
    # raises ValueError if there is no penguin for that player at the start Position or
    #   if the end position is not a valid move from the start Position
    def move_penguin(self, player, start_posn, end_posn):
        if start_posn in self.penguin_positions[player] and end_posn in self.board.get_valid_moves(start_posn, self.get_occupied_tiles()):
            # remove the tile from the board and add
            # the number of fish to this players score
            self.scores[player] += self.board.get_tile(start_posn)
            self.board.add_hole(start_posn)

            # update this players penguin positions while maintaining the
            # order of the list
            index = self.penguin_positions[player].index(start_posn)
            del self.penguin_positions[player][index]
            self.place_penguin(player, end_posn, index)

        else:
            raise ValueError("invalid move")

    # Applies a Move to the game state
    # Move -> Void
    # raises value error if the player attempting to move is not the current player
    def apply_move(self, move):
        if move[0] != self.get_current_player():
            raise ValueError("a player is attempting to move when it is no their turn")

        if len(move) == 2 and not move[1]:
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
        self.turn = (self.turn + 1) % len(self.players)

    # Returns whether or not the game is over, meaning no one can move.
    # Void -> Boolean
    def game_over(self):
        for player in self.players:
            if self.has_moves_left(player):
                return False
        return True

    # Returns whether or not a specific player has any available moves
    # Player -> Boolean
    def has_moves_left(self, player):
        for posn in self.penguin_positions[player]:
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

    def placable_position(self, position):
        return self.board.is_open(position, self.get_occupied_tiles())

    # Returns the list of Moves available to the current player.
    # Void -> List[Move]
    def get_current_player_valid_moves(self):
        player = self.get_current_player()
        player_moves = []

        if self.has_moves_left(player):
            for start_pos in self.penguin_positions[player]:
                end_positions = self.board.get_valid_moves(start_pos, self.get_occupied_tiles())
                for end_pos in end_positions:
                    player_moves.append((player, start_pos, end_pos))
        elif not self.game_over():
            player_moves = [(player, False)]

        return player_moves

    # Removes the given Player from the game
    # Player -> Void
    def remove_player(self, player):
        self.penguin_positions.remove(player)

        # Update the turn counter when removing a player from
        # the list of players
        index = self.players.index(player)
        if index < self.turn:
            self.turn -= 1

        self.players.remove(player)
        self.turn %= len(self.players)



    # Returns the GameState as the atomic data defined at the top of the file.
    # Void -> GameState
    def get_game_state(self):
        player_data = [player.get_data() for player in self.players]
        penguin_positions = {player.get_color(): positions for player, positions in self.penguin_positions.items()}
        player_scores = {player.get_color(): score for player, score in self.scores.items()}

        return (self.board.get_board_state(), player_data, penguin_positions, self.turn, player_scores)
