import copy

from Game.Common.board_interface import IBoard
from Game.Common.action import Action

class MarbleBoard(IBoard):
    """
    A MarbleBoard is a union of:
    - list(list(int)):
        2D list representing the 2D board layout with each cell containing either -1, 0, 1, where -1 represents the an invalid position off, a
        0 represents no game piece at that spot and 1 represents there is a
        game piece at that spot. 

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
    """

    def __init__(self):
        """Initializes a clean marble solitaire board with the cross configuration.
        """
        self.layout = self.generate_cross_layout()


    def generate_cross_layout(self):
        """Generates a cross layout for the marble board.

        Returns:
            list(list(int)): a 2D list representing the cross layout
        """
        cross_layout = []

        return cross_layout


    def valid_actions(self, player):
        """Finds a list of valid actions for the player on the marble board.

        Args:
            player (str): a color string representing the player

        Returns:
            list(Action): a list of actions
        """
        actions = []
        return actions

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
        return success, reward

    def serialize(self):
        """Serilizes the marbale board into a map of it's data representation.

        Returns:
            dict(X): a dictionary of attributes in the format specified as below:
            {
                "layout": list(list(int))
            }
        """
        return {
            "layout": copy.deepcopy(self.layout)
        }