import random
import time
import sys
sys.path.append('../../')

from Common.board import Board
from Common.state import GameState
from Common.Model.Player import Player
from Common.View.FishView import FishView

# A Position is a (Int, Int)
# It represents a location on the board, the first element being the rows
# and the second element being the column.

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

    # ?Int, ?Int, ?Boolean, ?Int, ?Int, ?Int, ?List[Position] -> Referee
    def __init__(self, rows=None, cols=None, uniform=False, uniform_fish_num=None, min_holes=0, min_one_fish=0,
                 specific_holes=[]):

        if rows is None:
            rows = random.randint(2, 7)
        if cols is None:
            cols = random.randint(2, 7)

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

        self.game_state = GameState([], self.board)

        self.fish_view = FishView(self.game_state.get_game_state())

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

if __name__ == '__main__':
    # short test script to make sure we can render the state graphically

    b = Board(3, 3, [[1, 2, 1], [1, 2, 5], [1, 1, 4]])
    player1 = Player(10, 'red')
    player2 = Player(15, 'brown')
    gs = GameState([player1, player2], b)

    fish_view = FishView(gs.get_game_state())
    fish_view.render()
    time.sleep(2)

    gs.place_penguin(player1, (1, 1))
    fish_view.update_game_state(gs.get_game_state())
    fish_view.render()
    time.sleep(2)

    gs.place_penguin(player2, (2, 1))
    fish_view.update_game_state(gs.get_game_state())
    fish_view.render()
    time.sleep(2)

    gs.move_penguin(player1, (1,1), (0,1))
    fish_view.update_game_state(gs.get_game_state())
    fish_view.render()
    time.sleep(2)
