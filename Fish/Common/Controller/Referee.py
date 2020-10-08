import random

class Referee:

    def __init__(self, rows=None, cols=None, uniform=False, uniform_fish_num = None, min_holes=0, min_one_fish=0, specific_holes = []):

        if not rows:
            rows = random.randint(2, 7)
        if not cols:
            cols = random.randint(2, 7)

        if rows < 1 or cols < 1:
            raise IllegalArgumentException("Rows and Cols must be a positive number")
        if (uniform and min_holes) or (uniform and min_one_fish):
            raise IllegalArgumentException("min_holes and min_one_fish areguments are not allowed when uniform is True")
        if uniform and not uniform_fish_num:
            raise IllegalArgumentException("A uniform board needs the uniform_fish_num specified in range [1, 5]")

        # Same number of fish everywhere, no holes
        self.board = None

        if uniform and type(uniform_fish_num) == int and uniform_fish_num <= 5 and uniform_fish_num >= 1:
            self.generate_uniform_board(rows, cols, uniform_fish_num)
        elif min_holes or min_one_fish:
            self.generate_non_uniform_board(rows, cols, min_holes, min_one_fish)
        elif specific_holes:
            pass
        else:
            rand_holes = random.randint(0, (rows + cols)//4)
            rand_one_fish = random.randint(0, (rows + cols)//4)
            self.generate_non_uniform_board(rows, cols, rand_holes, rand_one_fish)

        self.board_view = BoardView(self.board.get_board_state())


    def generate_uniform_board(self, rows, cols, fish_num):
        if rows < 1 or cols < 1:
            raise IllegalArgumentException("Cannot generate a uniform board with non-positive rows and columns")
        if fish_num < 1 or fish_num > 5:
            raise IllegalArgumentException("Uniform board must have between [1 and 5] fish")
        self.board = Board(rows, cols, num_fish=fish_num)

    def generate_non_uniform_board(self, rows, cols, min_holes, min_one_fish):
        board = Board(rows, cols, min_ones=min_one_fish)
        while board.hole_count() < min_holes:
            board.add_hole(random.randint(0, rows-1), random.randint(0, cols-1))
