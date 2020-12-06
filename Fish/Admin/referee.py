import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../.."))

from Fish.Common.board import Board
from Fish.Common.state import GameState
from Fish.Common.game_tree import GameTree
from Fish.Common.util import safe_execution
from Fish.Player.player import Player as AIPlayer
from Fish.Player.strategy import Strategy

from Fish.Admin.game_visualizer import GameVisualizer

# Action is one of:
# - Placement: (Color, Posn)
# - Movement: (Color, Posn, Posn)
# - Kick: (Color,)
# It represents a valid action in the game 

# A Posn is a (Int, Int)
# It represents a location on the board, the first element being the rows
# and the second element being the column.

# A Color is a String
# It is a string that represents the color that a player avatar get take

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
    def __init__(self, players, rows, cols, uniform=False, uniform_fish_num=None, min_holes=0, min_one_fish=0, specific_holes=None, observers=[]):

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
        self.action_update((color,))

    def is_kicked(self, color):
        return color in self.kicked_players

    # Performs the given placement if it is valid and returns true
    # else returns false
    # Placement -> Boolean
    def perform_placement(self, placement):
        if self.game_state.get_current_color() == placement[0] and self.game_state.placable_position(placement[1]):
            self.game_state.place_penguin(*placement)
            return True
        return False

    # Performs the given move if it is valid and returns true
    # else returns false
    # Move -> Void
    def perform_move(self, move):
        game_tree = GameTree(self.game_state)

        valid_moves = game_tree.get_children()
        if move in valid_moves.keys():
            self.game_state = valid_moves[move].get_current_state()
            return True
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
    # Void -> List[Player], List[Player]
    def run_game(self):
        self.update_color_assignments()
        self.update_initial_states()
        
        self.run_phase(self.PLACEMENT, self.perform_placement)

        self.run_phase(self.MOVEMENT, self.perform_move)

        winning_colors = self.game_state.get_winners()

        winning_players = [ player for color, player in self.color_to_player.items() if color in winning_colors ]
        
        cheating_failing_players = [ player for color, player in self.color_to_player.items() if color in self.kicked_players ]

        return (winning_players, cheating_failing_players)

    # Runs the given phase of the game until it's over, uses the given action handler
    # to perform the actions in this phase and kicks any players that failed to response
    # to action request to attempts to perform an invalid action
    # Void -> Void
    def run_phase(self, phase, action_handler):
        while self.get_gamephase() == phase:
            current_color = self.game_state.get_current_color()
            current_player = self.color_to_player[current_color]
            action, exc = safe_execution(self.action_requestor(current_player, phase))
            if action:
                success = action_handler(action)
                if success:
                    self.action_update(action)
                    continue
            self.kick_player(current_color)

    # Finds the proper action request handler for the player in the given game phase
    # Player, GamePhase -> Func
    def action_requestor(self, player, phase):
        requestor_table = {
            self.PLACEMENT: player.get_placement,
            self.MOVEMENT: player.get_move
        }
        return requestor_table[phase]

    # Updates each player on their color assignments
    def update_color_assignments(self):
        for color, player in self.color_to_player.items():
            ret, exc = safe_execution(player.color_assignment_update, [color])

    # Updates each player on the startup state of the game
    def update_initial_states(self):
        for player in self.color_to_player.values():
            ret, exc = safe_execution(player.inital_state_update, [self.game_state.get_game_state()])

        for observer in self.observers:
            observer.inital_state_update(self.game_state.get_game_state())

    # Updates all active players on the given action in the game
    # Action -> Void
    def action_update(self, action):
        action_key = len(action)
        
        for player in self.color_to_player.values():
            handler = self.action_update_handler(player, action_key)
            ret, exc = safe_execution(handler, [action])
        
        for observer in self.observers:
            handler = self.action_update_handler(observer, action_key)
            handler(action)

    # Finds the update handler for the given player or obserber using the action key
    # action key is an integer that identifies an action 
    # (Player or Observer), Int -> Func
    def action_update_handler(self, updator, action_key):
        handler_lookup = {
            1: updator.player_kick_update,
            2: updator.placement_update,
            3: updator.movement_update
        }
        return handler_lookup[action_key]


if __name__ == '__main__':
    # short test script to make sure we can render the state graphically
    rows = 5
    cols = 5
    players = [
        AIPlayer(Strategy, 20, "one"), 
        AIPlayer(Strategy, 16, "two"),
        AIPlayer(Strategy, 50, "three"),
        AIPlayer(Strategy, 27, "four"),
    ]
    observers = [GameVisualizer()]
    referee = Referee(players, rows, cols, observers=observers)

    winners = referee.run_game()
    for winner in winners:
        print("{} is a winner at age {}".format(winner.get_id(), winner.get_age()))
