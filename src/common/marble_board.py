import copy

from src.common.i_board import IBoard, BoardType
from src.common.action import action_type

class MarbleBoard(IBoard):
    """
    A MarbleBoard is a:
    - list(list(int)):
        2D list representing the 2D board layout with each cell containing either 0 or 1, where a 0 represents no game piece at that spot and 1 represents there is a game piece at that spot and 2 for any dead spot. 

    A MarbleBoard represents a square grid of tiles for the game of marble solitaire or peg solitaire (English Board) with layout of the indices as specified below:

    ╔═══════╤═══════╤═══════╗
    ║ (0,0) │ (0,1) │ (0,2) ║
    ╠═══════╪═══════╪═══════╣
    ║ (1,0) │ (1,1) │ (1,2) ║
    ╟───────┼───────┼───────╢
    ║ (2,0) │ (2,1) │ (2,2) ║
    ╚═══════╧═══════╧═══════╝

    This is a initial implementation of this type of board game only dealing with the popular cross configuration with 3x2 sizes as shown below:

        · · ·
        · · ·
    · · · · · · · 
    · · · o · · · 
    · · · · · · · 
        · · ·
        · · ·

    A MarbleBoard implements the IBoard interface.
    """
    
    HOLE = 0
    HAS_PIECE = 1
    INVALID = 2

    def __init__(self):
        """Initializes a clean marble solitaire board with the cross configuration.
        """
        self.width = 2
        self.height = 3
        self.size = 2 * self.width + self.height
        self.layout = self.generate_cross_layout()


    def generate_cross_layout(self):
        """Generates a cross layout for the marble board.

        Returns:
            list(list(int)): a 2D list representing the cross layout
        """
        cross_layout = []

        for r in range(self.size):
            cross_layout.append([])
            for c in range(self.size):
                if self.valid_posn((r,c)):
                    if not self.is_starting((r,c)):
                        cross_layout[r].append(self.HAS_PIECE)
                    else:
                        cross_layout[r].append(self.HOLE)
                else:
                    cross_layout[r].append(self.INVALID)

        return cross_layout

    def valid_posn(self, posn):
        """Determines whether the given position is a valid position on the marble board, this includes both out of board and the dead spots.

        Args:
            posn (Posn): a position to check

        Returns:
            bool: a boolean with true indicating that the position is valid and false otherwise
        """
        return self.in_bound(posn) \
                    and (self.in_middle_portion(posn) \
                            or self.in_side_portion(posn))

    def in_bound(self, posn):
        """Check whether the given position is in bound of the marble board.

        Args:
            posn (Posn): a position to check

        Returns:
            bool: a boolean with true indicating that it's in bound
        """
        return posn[0] < self.size and posn[0] >= 0 \
                    and posn[1] < self.size and posn[1] >= 0

    def in_middle_portion(self, posn):
        """Check whether the given position is in the middle portion of the marble board with valid column positions extending the whole size of the board. 

        Args:
            posn (Posn): a position to check

        Returns:
            bool: a boolean with true indicating that it's in the middle
        """
        return posn[0] >= self.width and posn[0] < (self.size - self.width)

    def in_side_portion(self, posn):
        """Check whether the given position is in the size portion of the marble board with valid column positions extending the just the side of the cross layout of the board. 

        Args:
            posn (Posn): a position to check

        Returns:
            bool: a boolean with true indicating that it's in the sid
        """
        return posn[1] >= self.width and posn[1] < (self.size - self.width) 

    def is_starting(self, posn):
        """Determines whether the given position is the starting empty position on the marble board.

        Args:
            posn (Posn): a position to check

        Returns:
            bool: a boolean with true indicating that the position is the starting empty position and false otherwise
        """
        return (posn[0] == 3) and (posn[1] == 3)

    def set_layout(self, layout):
        """Sets the layout of the board to the given one.

        Args:
            layout (2d list): 2d list of the board grid layout

        Returns:
            bool: a boolean with true indicating layout set successfully
        """
        try:
            self.layout = copy.deepcopy(layout)
            return True
        except Exception as e:
            print(e)
        return False

    def valid_actions(self, player):
        """Finds a list of valid actions for the player on the marble board, a valid action are any moves that a marble jumps over another into an empty spot.

        Args:
            player (str): a color string representing the player

        Returns:
            list(Action): a list of actions
        """
        return [(from_posn, hole) for hole in self.hole_positions() for from_posn in self.reachable_positions(hole)]

    def hole_positions(self):
        return [(r,c) for r in range(self.size) for c in range(self.size) if self.layout[r][c] == self.HOLE]

    def reachable_positions(self, from_hole):
        """Finds the list of reachable positions from the given hole on the marble board, a position is reachable from a hole if in a straight line the marble from the next position down has a marble to jump over.

        Args:
            from_hole (Posn): a position of a hole

        Returns:
            list(Posn): a list of positions reachable
        """
        reachable_positions = []
        directional_deltas = self.get_directional_deltas()

        for delta_r, delta_c in directional_deltas:
            stepping_stone = (from_hole[0] + delta_r, from_hole[1] + delta_c)
            if self.valid_posn(stepping_stone) \
                    and not self.empty(stepping_stone):
                from_posn = (stepping_stone[0] + delta_r, stepping_stone[1] + delta_c)
                if self.valid_posn(from_posn) and not self.empty(from_posn):
                    reachable_positions.append(from_posn)

        return reachable_positions

    def get_directional_deltas(self):
        """Finds the delta changes of one position for all 4 directional movements on the marble board. 

        Returns:
            list(tuple(int, int)): a list of delta changes where each element is a tuple of row and column delta change
        """
        return [(0, 1),(0, -1),(1, 0),(-1, 0)]

    def empty(self, posn):
        return self.layout[posn[0]][posn[1]] == self.HOLE

    def apply_action(self, player, action):
        """Applies the given action for the player on the marble board.

        Args:
            player (str): a color string reprenting the player
            action (Action): an action to apply

        Returns:
            tuple(bool, int): a tuple with the first a boolean indicating whether the action was successful and the second a reward if it was
        """
        success = False
        reward = 0

        if action_type(action).is_valid() \
                and action in self.valid_actions(player):
                        
            self.apply_jump(*action)
            reward = 1
            success = True

        return success, reward

    def apply_jump(self, from_posn, to_posn):
        """Applies the jump from the given positions on the marble board, updates the layout accordingly after the jump.

        Args:
            from_posn (Posn): a postion to jump from
            to_posn (Posn): a position to jump to
        """
        self.layout[to_posn[0]][to_posn[1]] = self.HAS_PIECE
        self.layout[from_posn[0]][from_posn[1]] = self.HOLE

        stepping_r, stepping_c = self.stepping_stone(from_posn, to_posn)
        self.layout[stepping_r][stepping_c] = self.HOLE

    def stepping_stone(self, from_posn, to_posn):
        """Finds the position between the from and to posn used as the stepping stone for the jump.

        Args:
            from_posn (Posn): a position
            to_posn (Posn): a position

        Returns:
            Posn: a position of the stepping stone
        """
        r = from_posn[0]
        c = from_posn[1]

        delta_r = to_posn[0] - from_posn[0]
        if delta_r != 0:
            r += 1 if delta_r > 0 else -1
        else:
            c += 1 if to_posn[1] > from_posn[1] else -1

        return r, c

    def game_over(self):
        """Determines if the game is over with the board state.

        Returns:
            bool: a boolean with true indicating the game is over
        """
        return (not self.valid_actions(""))

    def serialize(self):
        """Serilizes the marbale board into a map of it's data representation.

        Returns:
            dict(X): a dictionary of attributes in the format specified as below:
            {   
                "board-type": BoardType.value,
                "info": {
                    "layout: list(list(int)),
                }
            }
        """
        return {
            "board-type": BoardType.MARBLE.value,
            "info": {
                "layout": copy.deepcopy(self.layout),
            }
        }