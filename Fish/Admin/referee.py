import random
import time
import sys
sys.path.append('../')

from Common.board import Board
from Common.state import GameState
from Common.Model.Player import Player
from Player.player import Player as AIPlayer
from Player.strategy import Strategy
from Common.View.FishView import FishView

# A Position is a (Int, Int)
# It represents a location on the board, the first element being the rows
# and the second element being the column.

# Unnatural Conditions handled by the referee that result in a kick
# - Making a placement or move not during their respective GamePhases
# - Making an invalid move or placement

# Abnormal Conditions that will get you kicked by the communication layer
# - taking too long to make a move
# - too many messages withing a timeframe
# - closing the connection
# - attempting to make a move as another player

# A Referee controls the creation of the board and it also will handle when a player makes an invalid move
class Referee:

    # Generates a Referee given the options.
    #   Restrictions:
    #       if specified, rows and cols must be greater than 0
    #       if uniform is True, then uniform_fish_num must be specified as a number >= 1 and
    #           min_holes, min_one_fish and specific_holes must not be specified
    #       if specified uniform_fish_num must be in the range [1, 5]
    #       the total number tiles (rows * cols) must be greater than the number of required tiles
    #           (min_one_fish + max(min_holes, len(specific_holes))

    # List[Player], Int, Int, ?Boolean, ?Int, ?Int, ?Int, ?List[Position] -> Referee
    def __init__(self, players, rows, cols, uniform=False, uniform_fish_num=None, min_holes=0, min_one_fish=0,
                 specific_holes=[]):

        if rows < 1 or cols < 1:
            raise ValueError("Rows and Cols must be a positive number")
        if (uniform and min_holes) or (uniform and min_one_fish):
            raise ValueError("min_holes and min_one_fish areguments are not allowed when uniform is True")
        if uniform and not uniform_fish_num:
            raise ValueError("A uniform board needs the uniform_fish_num specified in range [1, 5]")
        if (max(min_holes, len(specific_holes)) + min_one_fish) > (rows * cols):
            raise ValueError("Too many specifications for this board size")

        self.board = Board(rows, cols)

        if uniform and type(uniform_fish_num) == int and uniform_fish_num <= 5 and uniform_fish_num >= 1:
            self.board.make_uniform_board(uniform_fish_num)
        elif min_one_fish:
            self.__generate_one_fish_limited_board(min_one_fish)
        else:
            self.board.make_random_board()

        if specific_holes or min_holes:
            self.__ensure_holes(specified_holes=specific_holes, min_holes=min_holes)

        self.board.assert_enough_ones(min_one_fish)

        self.game_state = GameState(players, self.board)

        self.fish_view = FishView(self.game_state.get_game_state())

        self.kicked_players = []
        self.__penguin_count = None

    # This method makes a board with a minimum number of 1 fish tiles.
    # This means the board will have a random number of fish everywhere and at least min_one_fish tiles
    #   with 1 fish on it
    # Int -> Void
    def __generate_one_fish_limited_board(self, min_one_fish):
        self.board.make_limited_board(min_one_fish)

    # This method makes sure the board will have the holes where it was specified and that there are enough holes
    # It does this by adding holes where they are specified, and then add random holes until we have enough.
    # List[Posn], Int -> void
    def __ensure_holes(self, specified_holes=None, min_holes=0):
        for hole in specified_holes:
            self.board.add_hole(hole)

        while self.board.hole_count() < min_holes:
            self.board.add_random_hole()

    # Removes a player from a game
    # Player -> Void
    def kick_player(self, player):
        self.game_state.remove_player(player)
        self.kicked_players.append(player)

    # Returns true if the color of the given player is kicked
    # Player -> Color
    def is_kicked(self, color):
        return color in [player.get_color() for player in self.kicked_players]

    # Performs the given placement if it is valid and during the placement phase
    # Kicks the player if it is invalid or not during placement phase
    # Player, Position -> Void
    def perform_placement(self, player, posn):
        if self.get_gamephase() == "placement":
            try:
                self.game_state.place_penguin(player, posn)
                return
            except ValueError:
                self.kick_player(player)
        else:
            self.kick_player(player)

    # Performs the given move if it is valid and during the playing phase
    # Kicks the player if it is invalid or not during playing phase
    # Player, Move -> Void
    def perform_move(self, move):
        if self.get_gamephase() == "playing":
            try:
                self.game_state.apply_move(move)
            except ValueError:
                self.kick_player(player)
        else:
            self.kick_player(player)

    # Returns the list of winners if the game is over.
    # If there is more than one player in the list, they are tied for first.
    # Void -> List[Player]
    def get_winners(self):
        if self.get_gamephase() == "finished":
            return self.game_state.get_winners()
        else:
            return False

    # Returns the current phase of the game.
    # Void -> List
    def get_gamephase(self):
        _, _, penguin_positions, _, _ = self.game_state.get_game_state()

        for color, penguins in penguin_positions.items():
            if len(penguins) < self.penguins_per_player():
                return "placement"

        if self.game_state.game_over():
            return "finished"

        return "playing"

    # Returns the current GameState
    # Void -> GameState
    def get_game_state(self):
        return self.game_state.get_game_state()

    # Helper methid to calculate how many penguins each player should have
    # Void -> Int
    def penguins_per_player(self):
        if not self.__penguin_count:
            _, players, _, _, _ = self.game_state.get_game_state()
            self.__penguin_count = 6 - (len(players) + len(self.kicked_players))

        return self.__penguin_count


if __name__ == '__main__':
    # short test script to make sure we can render the state graphically

    referee = Referee([Player(1, "red"), Player(4, "white"), Player(3, "brown"), Player(7, "black")], 6, 6)

    state = referee.get_game_state()
    fish_view = FishView(state)

    ais = {}
    for player in state[1]:
        ai = AIPlayer(Strategy)
        ai.set_color(player[1])
        ai.set_state(state)
        ais[player[1]] = ai

    # client side
    while referee.get_gamephase() != "finished":
        fish_view.update_game_state(referee.get_game_state())
        fish_view.render()
        time.sleep(2)

        for player, ai in ais.items():
            ai.set_state(referee.get_game_state())
            ai.set_gamephase(referee.get_gamephase())

            if ai.my_turn_huh():
                print("it muh turn")
                if ai.current_gamephase() == "placement":
                    # send to server
                    referee.perform_placement(player, ai.get_placement())
                elif ai.current_gamephase() == "playing":
                    # send to server
                    referee.perform_move(ai.get_move())
                break
