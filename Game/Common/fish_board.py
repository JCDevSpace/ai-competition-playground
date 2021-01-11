import copy
import random

from functools import reduce
from Game.Common.i_board import IBoard
from Game.Common.action import Action

class FishBoard(IBoard):
    """
    A FishBoard is a combination of: 
    - list(list(int)): 
        2D list representing the 2D board layout and the number of fish at each cell ranging from 1 to 5, and 0 indicating a hole at that position.
    - dict(str:list(Posn)):
        a map of color string representing a player and a list of all it's avatar positions.

    A FishBoard represents a hex grid of tiles for the board game fish with the layout of the indices as specified below:
     _____       _____       _____
    / 0,0 \_____/ 0,1 \_____/ 0,2 \_____
    \_____/ 1,0 \_____/ 1,1 \_____/ 1,2 
    / 2,0 \_____/ 2,1 \_____/ 2,2 \_____/
    \_____/     \_____/     \_____/

    A "OneTileMove" is a (Int, Int)
    It represents the change in position when moving a penguin one tile.

    There are two Lists[OneTileMoves], one for when the penguin is on an even row
    and one for when it is on an odd row. The indices in the array represents then
    direction of movement for the penguin in the following order:
    Down, Up, UpLeft, UpRight, DownLeft, DownRight.

    A FishBoard implements the IBoard interface.
    """
    PENGUIN_MAGIC = 6


    ODD_ROW_MOVES = [(2, 0), (-2, 0), (-1, 0), (-1, 1), (1, 0), (1, 1)]
    EVEN_ROW_MOVES = [(2, 0), (-2, 0), (-1, -1), (-1, 0), (1, -1), (1, 0)]

    HOLE = 0

    def __init__(self, players, rows, cols, layout=None, min_fish=1, max_fish=5, max_avatars=2):
        """Initializes a fish board, but information about the board itself is not avaialble until one of the make board method is called, if a preset layout is given, consumes it to fill in the layout and ignores given information about rows and cols, the preset layout given must satisfy the fish board requirements.

        Args:
            players (list(str)): a list of color string representing players
            rows (int): a positive integer representing how many rows to construct the board with
            cols (int): a positive integer representing how many columns to construct the board with
            layout (list(list(int)), optional): a 2d list for a preset layout. Defaults to None.
        """
        if layout:
            self.layout = layout
            self.rows = len(layout)
            self.cols = len(layout[0])
        else:
            self.layout = []
            self.rows = rows
            self.cols = cols

        self.avatars = {player:[] for player in players}
        self.movement_phase = False

        self.min_fish = min_fish
        self.max_fish = max_fish
        self.max_avatars = max_avatars

    def make_uniform_board(self, num_fish):
        """Makes the board with the same given number of fishes by modifying the internal layout, only works when the board was not initialized with a preset layout.

        Args:
            num_fish (int): a positive integer representing the number of fish to set each tile with
        
        Returns:
            bool: a boolean indicating whether the uniform board was filled successfully
        """
        if num_fish >= self.min_fish \
                and num_fish <= self.max_fish \
                and not self.layout:
            
            for y in range(self.rows):
                self.layout.append([])
                for _ in range(self.cols):
                    self.layout[y].append(num_fish)
            return True
        return False

    def make_limited_board(self, min_one_fish):
        """Makes the board with at least the given number of one fish tiles and the rest with a random number by modifying the internal layout, only works when the board was not initialized with a preset layout.

        Args:
            min_one_fish (int): a positive integer representing the number of one fish tiles to fill the board with

        Returns:
            bool: a boolean indicating whether the one fish board was filled successfully
        """
        return (min_one_fish > 0) \
                    and (not self.layout) \
                    and self.make_random_board() \
                    and self.make_ones(min_one_fish)

    def make_random_board(self):
        """Makes a board with a random number of fishes on each tile by modifying the internal layout, only works when the baord was not initialized with a preset layout.

        Returns:
            bool: a boolean indicating whether the random board was filled successfully
        """
        if not self.layout:
            for y in range(self.rows):
                self.layout.append([])
                for _ in range(self.cols):
                    self.layout[y].append(random.randint(self.min_fish, self.max_fish))
            return True
        return False

    def make_ones(self, min_ones):
        """Fill the board with one fish tiles until there are at least the given number by randomly picking a tile at a time and modifying to have one fish, fails when there's not enough tiles to achieve the given number or when there isn't an existing layout.

        Args:
            min_ones (int): a positive integer representing how one fish tiles to make

        Returns:
            bool: a boolean indicating whether the operation was successfuly
        """
        non_ones, holes = self.get_non_ones()

        non_holes = self.rows * self.cols - len(holes)
        if min_ones <= non_holes and self.layout:
            needed_num_ones = min_ones - non_holes + len(non_ones)
            if needed_num_ones > 0:
                self.replace_with_ones(non_ones, needed_num_ones)
            return True
        return False

    def get_non_ones(self):
        """Finds the list of tile positions that are not one fish tiles and the list of tile positions that are holes.

        Returns:
            tuple(list(Posn), list(Posn)): a tuple of position list with the first one being tiles that are not one fish and second tile that are holes
        """
        non_ones = []
        holes = []

        for r in range(self.rows):
            for c in range(self.cols):
                if self.layout[r][c] == self.HOLE:
                    holes.append((r,c))
                elif self.layout[r][c] != 1:
                    non_ones.append((r,c))

        return non_ones, holes

    def replace_with_ones(self, non_ones, num):
        """Replaces a number of tiles randomly from the given list of non one fish tiles with one fish tiles.

        Args:
            non_ones (list(Posn)): a list of position of non one fish tiles
            num (int): a positive integer of tiles for replace
        """
        sample_idxs = random.sample(range(len(non_ones)), num)
        for idx in sample_idxs:
            pos = non_ones[idx]
            self.layout[pos[0]][pos[1]] = 1

    def set_fish(self, count, posn):
        """Sets the fish count of the given valid position, only works when the layout information of the board is already filled, either by presets or with one of the make board methods.

        Args:
            count (int): a positive integer, >= min fish and <= max fish
            posn (Posn): a position on the board

        Returns:
            bool: a boolean indicating whether the fish count was set successfully
        """
        if self.valid_posn(posn) \
                and self.layout \
                and count >= self.min_fish \
                and count <= self.max_fish:

            self.layout[posn[0]][posn[1]] = count
            return True
        return False

    def set_hole(self, posn):
        """Sets the given position on the board as a hole, only works when the layout information of the board is already filled, either by presets or with one of the make board methods.

        Args:
            posn (Posn): a position to set the hole at

        Returns:
            bool: a boolean indicating whether the hole was set successfully
        """
        if self.valid_posn(posn) and self.layout:
            self.layout[posn[0]][posn[1]] = self.HOLE
            return True
        return False

    def set_random_hole(self):
        """Sets a random position on the board as a hole,only works when the layout information of the board is already filled, either by presets or with one of the make board methods.

        Returns:
            bool: a boolean indicating whether a random hole was successfully set
        """
        randrow = random.randint(0, self.rows - 1)
        randcol = random.randint(0, self.cols - 1)
        return self.set_hole((randrow, randcol))

    def valid_posn(self, posn):
        return 0 <= posn[0] < self.rows and 0 <= posn[1] < self.cols

    def reachable_positions(self, from_posn):
        """Finds the list of reachable positions from the given starting position, a position is reachable on the fish board if it's in a straight line from the starting position in any direction without holes inbetween and the position is not already occupied or a hole.

        Args:
            from_posn (Posn): a position to start from

        Returns:
            list(Posn): a list of positions reachable from the current position
        """
        reachable_positions = []

        for dir_index in range(len(self.ODD_ROW_MOVES)):
            reachable_positions += self.reachable_in_dir(from_posn, dir_index)
        
        return reachable_positions

    def reachable_in_dir(self, posn, dir_index):
        """Finds all the reachable position from the given starting position in a particular direction.

        Args:
            posn (Posn): a position to start from
            dir_index (int): a int of an index from the list of directions

        Returns:
            list(Posn): a list of positions reachable
        """
        if posn[0] % 2 == 1:
            moves = self.ODD_ROW_MOVES
        else:
            moves = self.EVEN_ROW_MOVES

        reachable_positions = []
        delta_row, delta_col = moves[dir_index]
        new_pos = (posn[0] + delta_row, posn[1] + delta_col)

        if self.non_edge(new_pos):
            if not self.is_occupied(new_pos):
                reachable_positions.append(new_pos)
            reachable_positions += self.reachable_in_dir(new_pos, dir_index)

        return reachable_positions

    def non_edge(self, posn):
        """Check whether the given position is not the edge of a the board, meaning that it's a valid board position and not a hole.

        Args:
            posn (Posn): a postion to check

        Returns:
            bool: a boolean indicating whether it's open or not
        """
        return self.valid_posn(posn) \
            and self.layout[posn[0]][posn[1]] != 0

    def is_occupied(self, posn):
        for positions in self.avatars.values():
            for position in positions:
                if position == posn:
                    return True
        return False

    def valid_actions(self, player):
        """Finds the list of valid action for the player on the fish board, required the layout information about the board to be filled with either presets or one of the make methods to work else it returns a empty list indicating there are no valid actions with the current fish board state.

        Args:
            player (str): a color string representing a player

        Returns:
            list(Action): a list of actions
        """
        actions = []

        if self.layout:
            actions.append(Action.SKIP)
            if self.movement_phase:
                if player in self.avatars:
                    actions += self.valid_movements(player)
            else:
                actions += self.valid_placements()
        return actions

    def valid_movements(self, player):
        """Finds a list of valid movement action on the fish board.

        Args:
            player (str): a color string representing a player

        Returns:
            list(Action): a list of movement actions
        """
        return [(from_posn, to_posn) for from_posn in self.avatars[player] for to_posn in self.reachable_positions(from_posn)]

    def valid_placements(self):
        """Finds a list of valid placement actions on the fish board.

        Args:
            player (str): a color string representing a player

        Returns:
            list(Action): a list of placement actions
        """
        return [(r,c) for r in range(self.rows) for c in range(self.cols) if self.layout[r][c] != self.HOLE and not self.is_occupied((r,c))]

    def apply_action(self, player, action):
        """Applies the given action for the player on the fish game board and calculates a reward if there is any.

        Args:
            player (str): a color string representing a player
            action (Action): an action to apply

        Returns:
            tuple(bool, int): a tuple with the first a boolean indicating whether the action was successfully applied and the second a reward if the action was successful
        """
        success = False
        reward = 0

        action_type = Action.type(action)

        if action_type != Action.INVALID \
                and action in self.valid_actions(player):

            if action_type == Action.MOVEMENT:
                reward =  self.apply_movement(player, action)
            elif action_type == Action.PLACEMENT:
                reward =  self.apply_placement(player, action)

            if not self.movement_phase and not self.in_placement():
                self.movement_phase = True

            success = True
        
        return success, reward

    def apply_movement(self, player, movement):
        """Applies the given movement action to the fish board and finds the corresponding reward.

        Args:
            player (str): a color string representing a player
            movement (Action): an action representing the movement to make

        Returns:
            int: a integer representing the reward associated with the action
        """
        from_posn, to_posn = movement

        avatar_idx = self.avatars[player].index(from_posn)
        self.avatars[player].pop(avatar_idx)
        self.avatars[player].insert(avatar_idx, to_posn)        
        
        self.layout[from_posn[0]][from_posn[1]] = self.HOLE

        return self.layout[to_posn[0]][to_posn[1]]

    def apply_placement(self, player, placement):
        """Applies the given placement action to the fish board and finds the corresponding reward.

        Args:
            player (str): a color string representing a player
            placement (Action): an action representing the placement to make

        Returns:
            int: a integer representing the reward associated with the action
        """
        self.avatars[player].append(placement)

        return self.layout[placement[0]][placement[1]]

    def in_placement(self):
        """Checks whether the current fish board state in still in the placement phase.

        Returns:
            bool: a bool representing with true representing still in placement phase
        """
        for player_avatars in self.avatars.values():
            if len(player_avatars) < self.max_avatars:
                return True
        return False

    def remove_player(self, player):
        """Removes the given player from game board.

        Args:
            player (str): a color string representing a player

        Returns:
            bool: a boolean with true indicating the player was successfully removed
        """
        if player in self.avatars:
            del self.avatars[player]
            return True
        return False

    def game_over(self):
        """Determines if the game is over with the board state.

        Returns:
            bool: a boolean with true indicating the game is over
        """
        if len(self.avatars) > 1:
            skip_only = True
            for player in self.avatars.keys():
                actions = self.valid_actions(player)
                if actions:
                    if len(actions) != 1:
                        skip_only = False
                    
                    if not skip_only:
                        return False
            
        return True

    def serialize(self):
        """Serializes the fish board into a dict it's data representation.

        Returns:
            dict(X): a dictionary of attributes in the format specified as below:
            {
                "layout: list(list(int)),
                "avatars": dict(str:list(Posn))
            }
        """
        return {
            "layout": copy.deepcopy(self.layout),
            "avatars": copy.deepcopy(self.avatars),
        }
