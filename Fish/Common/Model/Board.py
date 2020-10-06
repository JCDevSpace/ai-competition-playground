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

    def __init__(self, rows, cols, num_fish=None):
        layout = []
        for y in range(rows):
            layout.append([])
            for x in range(cols):
                if num_fish:
                    layout[y].append(num_fish)
                else:
                    layout[y].append(random.randint(1, 5))

        self.layout = layout

    ## Pregame methods
    def add_hole(self, row, col):
        self.layout[row][col] = -1

    def set_fish(self, num_fish, row, col):
        self.layout[row][col] = num_fish

    def place_penguin(self, player, row, col) -> int:
        #Returns the number of fish from that tiles
        score = self.layout[row][col]
        self.layout[row][col] = player.get_color()
        return score

    # Play methods

    def remove_penguin(self, player, row, col):
        if self.layout[row][col] == player.get_color():
            self.layout[row][col] = -1
        else:
            raise IllegalArgumentException("Cannot remove another player's penguin")

    def move(self, player, old_row, old_col, new_row, new_col):
        if (new_row, new_col) in self.get_valid_moves(player, old_row, old_col, new_row, new_col):
            self.remove_penguin(player, old_row, old_col)
            return self.place_penguin(player,new_row, new_col)
        else:
            raise IllegalArgumentException("bad move")


    def get_valid_moves(self, player, row, col):
        if self.layout[row][col] != player.get_color():
            return []
        else:
            pass

    def get_board_state(self):
        return self.layout
