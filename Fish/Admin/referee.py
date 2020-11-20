import random
import time
import sys

sys.path.append('..')

from Fish.Common.board import Board
from Fish.Common.state import GameState
from Fish.Common.game_tree import GameTree
from Fish.Common.message import Message
from Fish.Player.player import Player as AIPlayer
from Fish.Player.strategy import Strategy


# A Position is a (Int, Int)
# It represents a location on the board, the first element being the rows
# and the second element being the column.

# Unnatural Conditions handled by the referee that result in a kick
# - Making an invalid move or placement

# Abnormal Conditions that will get you kicked by the communication layer
# - taking too long to make a move
# - too many messages withing a timeframe
# - closing the connection

# A Referee controls the creation of the board and it also will handle when a player makes an invalid move.
# When initialized with a list of players, can find the results of a whole game by using the
# run_game() method
class Referee:
    COLORS = ["red", "brown", "white", "black"]
    MAGIC_PENGUIN_NUMBER = 6

    # GamePhases
    PLACEMENT = "placement"
    MOVEMENT = "movement"
    FINISHED = "finished"

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
                 specific_holes=None, observers=[]):

        if len(players) > 4 or len(players) < 2:
            raise ValueError("Invalid number of players")

        if not specific_holes:
            specific_holes = []

        if rows < 1 or cols < 1:
            raise ValueError("Rows and Cols must be a positive number")
        if (uniform and min_holes) or (uniform and min_one_fish):
            raise ValueError("min_holes and min_one_fish areguments are not allowed when uniform is True")
        if uniform and not uniform_fish_num:
            raise ValueError("A uniform board needs the uniform_fish_num specified in range [1, 5]")
        if (max(min_holes, len(specific_holes)) + min_one_fish) > (rows * cols):
            raise ValueError("Too many specifications for this board size")

        self.board = Board(rows, cols)

        if uniform and type(uniform_fish_num) == int and 5 >= uniform_fish_num >= 1:
            self.board.make_uniform_board(uniform_fish_num)
        elif min_one_fish:
            self.__generate_one_fish_limited_board(min_one_fish)
        else:
            self.board.make_random_board()

        if specific_holes or min_holes:
            self.__ensure_holes(specified_holes=specific_holes, min_holes=min_holes)

        self.board.assert_enough_ones(min_one_fish)

        self.color_to_player = {}
        turn_order = []
        for index, player in enumerate(players):
            self.color_to_player[self.COLORS[index]] = player
            turn_order.append(self.COLORS[index])

        self.game_state = GameState(self.board, turn_order)

        self.kicked_players = []

        # inititialize the number of penguins each player should have on the board
        # shouldn't change when players get kicked
        self.__penguin_count = self.__penguins_per_player()

        if rows * cols - max(min_holes, len(specific_holes)) < len(players) * self.__penguin_count:
            raise ValueError("Too many holes for this number of penguin")

        self.observers = observers

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

    # Helper method to calculate how many penguins each player should have
    # Void -> Int
    def __penguins_per_player(self):
        _, players, _, _, _ = self.game_state.get_game_state()
        self.__penguin_count = self.MAGIC_PENGUIN_NUMBER - (len(players) + len(self.kicked_players))

        return self.__penguin_count

    # Removes a player from a game and informs all other players
    # that the color was kicked.
    # Color -> Void
    def kick_player(self, color):
        self.game_state.remove_player(color)
        self.kicked_players.append(color)
        self.update_players(Message.generate_kick(color))

    def is_kicked(self, color):
        return color in self.kicked_players

    # Performs the given placement if it is valid ans returns true
    # Kicks the player if it is invalid and returns false
    # (Color, Position) -> Boolean
    def perform_placement(self, placement):
        if self.game_state.get_current_color() == placement[0] and self.game_state.placable_position(placement[1]):
            self.game_state.place_penguin(*placement)
            return True
        else:
            self.kick_player(placement[0])
            return False

    # Performs the given move if it is valid and returns true
    # Kicks the player if it is invalid and returns false
    # Move -> Void
    def perform_move(self, move):
        game_tree = GameTree(self.game_state)

        valid_moves = game_tree.get_children()
        if move in valid_moves.keys():
            self.game_state = valid_moves[move].get_current_state()
            return True
        else:
            self.kick_player(move[0])
            return False

    # Returns the current phase of the game.
    # Void -> List
    def get_gamephase(self):
        _, _, penguin_positions, _, _ = self.game_state.get_game_state()

        for color, penguins in penguin_positions.items():
            if len(penguins) < self.__penguin_count:
                return self.PLACEMENT

        if self.game_state.game_over():
            return self.FINISHED

        return self.MOVEMENT

    # Runs an entire game of Fish using the players this was initialized with
    # and returns the winners of the game. If there is a tie, it returns a multiple players.
    # Void -> List[Player]
    def run_game(self):
        # tell players what their color is and the initial state of the board
        self.assign_colors()
        self.set_initial_states()
        
        # get all placements from players
        self.run_placement_phase()

        # get movements from players until the game is over
        self.run_movement_phase()

        # return winners
        winning_colors = self.game_state.get_winners()
        return [ player for color, player in self.color_to_player.items() if color in winning_colors ]
    
    # Runs the placement phase of the game, kicks players for invalid placements
    #and failure to communicate
    # Void -> Void
    def run_placement_phase(self):
        while self.get_gamephase() == self.PLACEMENT:
            current_color = self.game_state.get_current_color()
            current_player = self.color_to_player[current_color]
            placement = current_player.get_placement()

            if placement:
                success = self.perform_placement(placement)
                if success:
                    self.update_players(Message.generate_placement(placement))
            else:
                # communication error
                self.kick_player(current_color)

    # Runs the movement phase of the game, kicks players for invalid moves
    # and failure to communicate
    # Void -> Void
    def run_movement_phase(self):
        while self.get_gamephase() == self.MOVEMENT:
            current_color = self.game_state.get_current_color()
            current_player = self.color_to_player[current_color]
            move = current_player.get_move()

            if move:
                success = self.perform_move(move)
                if success:
                    self.update_players(Message.generate_movement(move))
            else:
                # communication error
                self.kick_player(current_color)


    # Assigns all players in the game their color
    # If a player fails to receive the message they get kicked
    # Void -> Void
    def assign_colors(self):
        for color, player in self.color_to_player.items():
            success = player.send_message(Message.generate_color_assignment(color))
            if not success:
                self.kick_player(color)

    # Sends each player the given message
    # If a player fails to receive the message they get kicked
    # Message -> Void
    def update_players(self, message):
        for color, player in self.color_to_player.items():
            success = player.send_message(message)
            if not success:
                self.kick_player(color)

    def set_initial_states(self):
        self.update_players(Message.generate_initial_state(self.game_state.get_game_state()))

    # Updates all the observers' game states
    # Void -> Void
    #def __update_observers(self):
    #    for observer in self.observers:
    #        observer.update_game_state(self.get_game_state())




if __name__ == '__main__':
    # short test script to make sure we can render the state graphically
    referee = Referee([AIPlayer(Strategy, 4), AIPlayer(Strategy, 5)], 5, 5)

    print(referee.run_game())
