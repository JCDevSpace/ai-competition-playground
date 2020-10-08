import random

class Board:

'''
0   1   2
  3   4   5
6   7   8
  9   10  11

[[0, 1, 2],
 [3, 4, 5],
 [6, 7, 8],
 [9, 10, 11]]

'''
# Layout : List[List[Tile]]
#   Tile is one of (Int, Color)
#       Color is one of "red", "white", "brown", "black"

    def __init__(self, rows, cols, num_fish=None, min_ones = 0):
        layout = []
        ones = 0
        for y in range(rows):
            layout.append([])
            for x in range(cols):
                if num_fish:
                    layout[y].append(num_fish)
                else:
                    layout[y].append(random.randint(1,5))

        self.layout = layout
        self.rows = rows
        self.cols = cols
        self.min_ones = min_ones

        self.odd_row_moves = [(2, 0), (-2, 0), (-1, 0), (-1, 1), (1, 0), (1, 1)]
        self.even_row_moves= [(2, 0), (-2, 0), (-1, -1), (-1, 0), (1, -1), (1, 0)]

        self.assert_enough_ones()


    ## Pregame methods

    def assert_enough_ones(self, min_ones=self.min_ones):
        ones = 0
        for y in range(self.rows):
            for x in range(self.cols):
                if self.layout[y][x] == 1:
                    ones += 1

        while ones < self.min_ones:
            randrow = random.randint(0, rows-1)
            randcol = random.randint(0, cols-1)
            if self.layout[randrow][randcol] != 1:
                self.layout[randrow][randcol] = 1
                ones += 1

    def add_hole(self, row, col):
        self.layout[row][col] = -1
        self.assert_enough_ones()

    def set_fish(self, num_fish, row, col):
        self.layout[row][col] = num_fish

    def place_penguin(self, player, row, col) -> int:
        #Returns the number of fish from that tiles
        score = self.layout[row][col]
        self.layout[row][col] = player.get_color()
        return score

    def hole_count(self):
        holes = 0
        for y in range(self.rows):
            for x in range(self.cols):
                if self.layout[y][x] == -1:
                    holes += 1
        return holes

        
    # Play methods

    def remove_penguin(self, player, row, col):
        if self.layout[row][col] == player.get_color():
            self.layout[row][col] = -1
        else:
            raise IllegalArgumentException("Cannot remove another player's penguin")

    def move(self, player, old_row, old_col, new_row, new_col):
        if (new_row, new_col) in self.get_valid_moves(player, old_row, old_col):
            self.remove_penguin(player, old_row, old_col)
            return self.place_penguin(player,new_row, new_col)
        else:
            raise IllegalArgumentException("bad move")


    def get_valid_moves(self, player, row, col):
        if self.layout[row][col] != player.get_color():
            return []
        else:
            valid_moves = []
            for dir_index in range(len(self.odd_row_moves)):
                valid_moves += self.valid_in_dir(row, col, dir_index)
            return valid_moves

    def is_valid_square(self, row, col):
        row_valid = row >= 0 and row <  self.rows
        col_valid = col >= 0 and col < self.cols
        square_valid = type(self.layout[row][col]) == int and self.layout[row][col] >= 1
        return row_valid and col_valid and square_valid


    def valid_in_dir(self, row, col, dir_index):
        if row % 2 == 1:
            moves = self.odd_row_moves
        else:
            moves = self.even_row_moves
        valid_moves = []
        (delta_row, delta_col) = moves[dir_index]
        new_pos = (row + delta_row, col + delta_col)

        if self.is_valid_square(new_pos[0], new_pos[1]):
            valid_moves.append(new_pos)
            valid_moves += self.valid_in_dir(new_pos[0], new_pos[1], dir_index)

        return valid_moves

    def get_board_state(self):
        return self.layout
