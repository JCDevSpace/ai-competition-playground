# import random
#
# # Board : List[List[Tile]]
# # The Board represents a hex grid of tiles.
# # The layout of the indices is as follows:
# #  _____       _____       _____
# # / 0,0 \_____/ 0,1 \_____/ 0,2 \_____
# # \_____/ 1,0 \_____/ 1,1 \_____/ 1,2 \
# # / 2,0 \_____/ 2,1 \_____/ 2,2 \_____/
# # \_____/     \_____/     \_____/
#
#
# # A Tile is an Int between -1 and 5
# # -1 represents a hole in the grid.
# # A 0 represents a tile with no fish.
# # And a number between 1 - 5 represents the number of fish on that tile
#
# # A Position is a (Int, Int)
# # It represents a location on the board, the first element being the rows
# # and the second element being the column.
#
# class Board:
#     # A "OneTileMove" is a (Int, Int)
#     # It represents the change in position when moving a penguin one tile.
#
#     # There are two Lists[OneTileMoves], one for when the penguin is on an even row
#     # and one for when it is on an odd row. The indices in the array represents then
#     # direction of movement for the penguin in the following order:
#     # Down, Up, UpLeft, UpRight, DownLeft, DownRight
#
#     ODD_ROW_MOVES = [(2, 0), (-2, 0), (-1, 0), (-1, 1), (1, 0), (1, 1)]
#     EVEN_ROW_MOVES = [(2, 0), (-2, 0), (-1, -1), (-1, 0), (1, -1), (1, 0)]
#
#     # Initialized a board, after calling init there is no board yet, one of the make_*_board methods
#     #   has to be called first
#     # Int, Int, ?Board -> Board
#     def __init__(self, rows, cols, layout=None):
#         if layout:
#             self.layout = layout
#             self.rows = len(layout)
#             self.cols = len(layout[0])
#         else:
#             self.layout = []
#             self.rows = rows
#             self.cols = cols
#         self.min_one_fish = 0
#
#     # Fills out the board's internal representation of the board to have the same number of fish
#     #   (num_fish) on every tile
#     # Modifies internal self.layout
#     # Int -> Void
#     def make_uniform_board(self, num_fish):
#         for y in range(self.rows):
#             self.layout.append([])
#             for x in range(self.cols):
#                 self.layout[y].append(num_fish)
#
#     # Fills out the board's internal representation of the board to have a minimum number of tiles with exactly one fish on it
#     # The board will have a random number of fish on the rest of the tiles
#     # Modifies interval self.layout and self.min_one_fish
#     # Int -> Void
#     def make_limited_board(self, min_one_fish):
#         self.min_one_fish = min_one_fish
#         self.make_random_board()
#         self.assert_enough_ones(min_one_fish)
#
#     # Fills out the board's internal representation of the board to have a random number of fish on all of the tiles
#     # Modifies interval self.layout
#     # Void -> Void
#
#     def make_random_board(self):
#         for y in range(self.rows):
#             self.layout.append([])
#             for x in range(self.cols):
#                 self.layout[y].append(random.randint(1, 5))
#
#     # This method makes sure that the board has enough one fish tiles
#     # it does this by setting a random tile to have 1 fish until there are enough
#     # Modifies internal self.layout. It is possible all non-hole could be changed to 1's
#     # Int -> Void
#     # raises ValueError if attempting to assert too many ones
#     def assert_enough_ones(self, min_ones):
#         if min_ones > self.rows * self.cols - self.hole_count():
#             raise ValueError(f"Not enough fish tiles to assert {min_ones} one fish tiles")
#
#         ones = 0
#         for y in range(self.rows):
#             for x in range(self.cols):
#                 if self.layout[y][x] == 1:
#                     ones += 1
#
#         while ones < min_ones:
#             randrow = random.randint(0, self.rows - 1)
#             randcol = random.randint(0, self.cols - 1)
#             if self.layout[randrow][randcol] != 1 and self.layout[randrow][randcol] != -1:
#                 self.layout[randrow][randcol] = 1
#                 ones += 1
#
#     # Returns the tile at the given Position
#     # Position -> Tile
#     # raises ValueError if Position not on the board
#     def get_tile(self, posn):
#         if self.valid_posn(posn):
#             return self.layout[posn[0]][posn[1]]
#         else:
#             raise ValueError(f"Invalid position {posn}")
#
#     # Sets the number of fish at a given Position
#     # Modifies internal self.layout
#     # Position -> Void
#     # raises ValueError if Position is not on the board
#     def set_fish(self, count, posn):
#         if self.valid_posn(posn):
#             self.layout[posn[0]][posn[1]] = count
#         else:
#             raise ValueError(f"Invalid position {posn}")
#
#     # Creates a hole at a given Position
#     # Modifies internal self.layout
#     # Position -> Void
#     # raises ValueError if Position is not in board
#     def add_hole(self, position):
#         if self.valid_posn(position):
#             self.layout[position[0]][position[1]] = -1
#         else:
#             raise ValueError(f"Invalid Position {position}")
#
#     # Adds a hole at a random Position
#     # Modifies internal self.layout
#     # Void -> Void
#     def add_random_hole(self):
#         randrow = random.randint(0, self.rows - 1)
#         randcol = random.randint(0, self.cols - 1)
#         self.add_hole((randrow, randcol))
#
#     # Returns the count of holes in the Board
#     # Void -> Int
#     def hole_count(self):
#         holes = 0
#         for y in range(self.rows):
#             for x in range(self.cols):
#                 if self.layout[y][x] == -1:
#                     holes += 1
#         return holes
#
#     # Returns the list of Positions reachable from the given Position
#     # Position -> List[Position]
#     def get_valid_moves(self, posn):
#         valid_moves = []
#         for dir_index in range(len(self.ODD_ROW_MOVES)):
#             valid_moves += self.valid_in_dir(posn, dir_index)
#         return valid_moves
#
#     # Returns whether or not a Position is on the board, makes no promises of the state of that tile
#     # Position -> Boolean
#     def valid_posn(self, posn):
#         return 0 <= posn[0] < self.rows and 0 <= posn[1] < self.cols
#
#     # Returns whether or not a Positon is open for a penguin to jump on, meaning there is not a
#     #   hole or another penguin at that position and it is a valid Position on this board
#     # Position -> Boolean
#     def is_open(self, posn):
#         return self.valid_posn(posn) and self.get_tile(posn) >= 1
#
#     # Returns all the valid Positions to jump to from the given starting Position in a particular direction
#     # the direction is an index which corresponds to a set of OneTileMoves from the *_ROW_MOVES lists.
#     # Position, Int -> List[Position]
#     def valid_in_dir(self, posn, dir_index):
#         if posn[0] % 2 == 1:
#             moves = self.ODD_ROW_MOVES
#         else:
#             moves = self.EVEN_ROW_MOVES
#         valid_moves = []
#         (delta_row, delta_col) = moves[dir_index]
#         new_pos = (posn[0] + delta_row, posn[1] + delta_col)
#
#         if self.is_open(new_pos):
#             valid_moves.append(new_pos)
#             valid_moves += self.valid_in_dir(new_pos, dir_index)
#
#         return valid_moves
#
#     # Returns the board state as a Board as specified at the top of the file
#     # Void -> Board
#     def get_board_state(self):
#         return self.layout
