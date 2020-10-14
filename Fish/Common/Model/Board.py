import random

# Board : List[List[Tile]]
# The Board represents a hex grid of tiles.
# The layout of the indeces is as follows:
#  _____       _____       _____
# / 0,0 \_____/ 0,1 \_____/ 0,2 \_____
# \_____/ 1,0 \_____/ 1,1 \_____/ 1,2 \
# / 2,0 \_____/ 2,1 \_____/ 2,2 \_____/
# \_____/     \_____/     \_____/


# A Tile is an Int between -1 and 5
# -1 represents a hole in the grid.
# A 0 represents a tile with no fish.
# And a number between 1 - 5 represents the number of fish on that tile

# A Position is a (Int, Int)
# It represents a location on the board, the first element being the rows
# and the second element being the column.

class Board:
    # A "OneTileMove" is a (Int, Int)
    # It represents the change in position when moving a penguin one tile.

    # There are two Lists[OneTileMoves], one for when the penguin is on an even row
    # and one for when it is on an odd row. The indeces in the array represnts then
    # direction of movement for the penguin in the following order:
    # Down, Up, UpLeft, UpRight, DownLeft, DownRight

    ODD_ROW_MOVES = [(2, 0), (-2, 0), (-1, 0), (-1, 1), (1, 0), (1, 1)]
    EVEN_ROW_MOVES = [(2, 0), (-2, 0), (-1, -1), (-1, 0), (1, -1), (1, 0)]

    def __init__(self, rows, cols):
        self.layout = []
        self.rows = rows
        self.cols = cols
        self.min_one_fish = 0

    def make_uniform_board(self, num_fish):
        for y in range(self.rows):
            self.layout.append([])
            for x in range(self.cols):
                self.layout[y].append(num_fish)

    def make_limited_board(self, min_one_fish):
        self.min_one_fish
        self.make_random_board()
        self.assert_enough_ones(min_one_fish)

    def make_random_board(self):
        for y in range(self.rows):
            self.layout.append([])
            for x in range(self.cols):
                self.layout[y].append(random.randint(1, 5))

    # This method makes sure that the board has enough one fish tiles
    # it does this by setting a random tile to have 1 fish until there are enough
    def assert_enough_ones(self, min_ones):
        ones = 0
        for y in range(self.rows):
            for x in range(self.cols):
                if self.layout[y][x] == 1:
                    ones += 1

        while ones < min_ones:
            randrow = random.randint(0, self.rows-1)
            randcol = random.randint(0, self.cols-1)
            if self.layout[randrow][randcol] != 1 and self.layout[randrow][randcol] != -1:
                self.layout[randrow][randcol] = 1
                ones += 1

    def get_tile(self, posn):
        return self.layout[posn[0]][posn[1]]

    def set_fish(self, count, posn):
        self.layout[posn[0]][posn[1]] = count

    def add_hole(self, position):
        self.layout[position[0]][position[1]] = -1

    def add_random_hole(self):
        randrow = random.randint(0, self.rows -1)
        randcol = random.randint(0, self.cols -1)
        self.add_hole((randrow, randcol))

    def hole_count(self):
        holes = 0
        for y in range(self.rows):
            for x in range(self.cols):
                if self.layout[y][x] == -1:
                    holes += 1
        return holes

    def get_valid_moves(self, posn):
        valid_moves = []
        for dir_index in range(len(self.ODD_ROW_MOVES)):
            valid_moves += self.valid_in_dir(posn, dir_index)
        return valid_moves

    def valid_posn(self, posn):
        return posn[0] >= 0 and posn[0] < self.rows and posn[1] >= 0 and posn[1] < self.cols

    def is_open(self, posn):
        return self.valid_posn(posn) and self.get_tile(posn) >= 1

    def valid_in_dir(self, posn, dir_index):
        if posn[0] % 2 == 1:
            moves = self.ODD_ROW_MOVES
        else:
            moves = self.EVEN_ROW_MOVES
        valid_moves = []
        (delta_row, delta_col) = moves[dir_index]
        new_pos = (posn[0] + delta_row, posn[1] + delta_col)

        if self.is_open(new_pos):
            valid_moves.append(new_pos)
            valid_moves += self.valid_in_dir(new_pos, dir_index)

        return valid_moves

    def get_board_state(self):
        return self.layout
