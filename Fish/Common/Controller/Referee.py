import random
from Model.Board import Board
from View.BoardView import BoardView

class Referee:

    def __init__(self, rows=None, cols=None, uniform=False, uniform_fish_num = None, min_holes=0, min_one_fish=0, specific_holes = []):

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
        if (max(min_holes, len(specific_holes)) + min_one_fish) >  (rows * cols):
            raise ValueError("Too many specifications for this board size")


        self.board = Board(rows,  cols)

        if uniform and type(uniform_fish_num) == int and uniform_fish_num <= 5 and uniform_fish_num >= 1:
            self.board.make_uniform_board(uniform_fish_num)
        elif min_one_fish:
            self.__generate_one_fish_limited_board(min_one_fish)
        else:
            self.board.make_random_board()

        if specific_holes or min_holes:
            self.__ensure_holes(specified_holes=specific_holes, min_holes=min_holes)


        self.board.assert_enough_ones(min_one_fish)

        self.board_view = BoardView(self.board.get_board_state())


    def __generate_one_fish_limited_board(self, min_one_fish):
        self.board.make_limited_board(min_one_fish)

    def __ensure_holes(self, specified_holes=None, min_holes=0):
        for hole in specified_holes:
            self.board.add_hole(hole[0], hole[1])

        while self.board.hole_count() < min_holes:
            self.board.add_random_hole()
