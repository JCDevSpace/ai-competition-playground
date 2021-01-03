import copy

from Game.Common.board_interface import IBoard
from Game.Common.action import Action


class ChessBoard(IBoard):
    """
    A ChessBoard is a union of:
    - list(list(int)):
        2D list representing the 2D board layout with each cell containing an integer ranging from 0 to 6, where 0 represents no game piece at that spot and 1 to 6 correspondes to a type of unique piece of chess with the mapping as specified below:
        
        1: The Pawn
        2: The Bishop
        3: The Knight
        4: The Rook
        5: The Queen
        6: The King

    - dict(str:list(Posn)):
        a map of color strings white and black representing a player and a list of all their avatar positions.

    A FishBoard represents a square grid of tiles for the game of chess with layout of the indices as specified below:

    ╔═══════╤═══════╤═══════╗
    ║ (0,0) │ (0,1) │ (0,2) ║
    ╠═══════╪═══════╪═══════╣
    ║ (1,0) │ (1,1) │ (1,2) ║
    ╟───────┼───────┼───────╢
    ║ (2,0) │ (2,1) │ (2,2) ║
    ╚═══════╧═══════╧═══════╝

    A ChessBoard implements the IBoard interface.
    """

    HOLE = 0
    PAWN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

    def __init__(self):
        """Initializes a chess board with the default configuration and pieces.
        """
        self.size = 8
        self.avatars = self.generate_default_placement()
        self.layout = self.generate_default_layout()

    def generate_default_placement(self):
        """Generates the default placement of all chess pieces.

        Returns:
            dict: a dictionary containing all the default avatar position for the players
        """
        avatars = {"black":[], "white":[]}
        
        for r in range(self.size):
            for c in range(self.size):
                if self.in_white_start(r,c):
                    avatars["white"].append((r,c))
                elif self.in_black_start(r,c):
                    avatars["black"].append((r,c))

        return avatars

    def generate_default_layout(self):
        """Generates the default chess board layout.

        Returns:
            list(list(int)): a 2D list representing the layout 
        """
        return [
            [4,3,2,6,5,2,3,4],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1],
            [4,3,2,6,5,2,3,4]
        ]

    def valid_actions(self, player):
        """Finds the list of valid action for the player on the chess board, returns an empty list if there are no valid actions meaning that the game is over.

        Args:
            player (str): a color string representing a player

        Returns:
            list(Action): a list of actions that can be performed
        """
        actions = []

        if player in self.avatars:
            for from_posn in self.avatars[player]:
                reachable_generator = self.get_reachable_generator(self.layout[from_posn[0]][from_posn[1]])
                for to_posn in reachable_generator(from_posn):
                    actions.append((from_posn, to_posn))

        return actions

    def reachable_generator(self, type_encoding, from_posn):
        """Finds the position generator that takes a starting position and generates all it's reachable positions for the given encoded chess piece type.

        Args:
            type_encoding (int): a integer representing the encoding of the chess piece type as specified in class intepretation
            from_posn (Posn): a position for the generator to use as the starting position

        Returns:
            function: a generator function
        """
        generator_table = {
            1:self.pawn_reachable_generator,
            2:self.bishop_reachable_generator,
            3:self.knight_reachable_generator,
            4:self.rook_reachable_generator,
            5:self.queen_reachable_generator,
            6:self.king_reachable_generator,
        }
        return generator_table[type_encoding](from_posn)

    def apply_action(self, player, action):
        """Applies the given action for the player on the current game board and returns a reward if there is any.

        Args:
            action (Action): an action to apply

        Returns:
            tuple(bool, int): a tuple with the first a boolean indicating whether the action was successful and the second a reward if the action was successfuly.
        """
        pass

    def serialize(self):
        """Serializes information about the current chess board to a map of attritube with corresponding values.

        Returns:
            dict(X): a dictionary with attributes in the format specified as below:
            {
                "layout: list(list(int)),
                "avatars": map(str:list(Posn))
            }
        """
        return {
            "layout": copy.deepcopy(self.layout),
            "avatars": copy.deepcopy(self.avatars),
        }