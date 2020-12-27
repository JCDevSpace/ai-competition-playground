class IBoard:
    """A IBoard represents the board of a board game, keeping track of board dimensions, board configuration/arrangement and game piece positions on the board.

    A Posn is a (Int, Int)
    It represents a 2D coordinate on a game board, where the first element is the row and the second the column positions, both row and column has to be greater or equal to 0.

    An Action is one of:
    - False: for a skip action
    - Posn: for placing a player avatar at a position
    - (Posn, Posn): for moving a player avatar from Posn one to another
    It represents an action that a player can take on the board.
    """

    def valid_actions(self, player):
        """Finds the list of valid action for the given player.

        Args:
            player (str): a color string representing a player

        Returns:
            list(Action): a list of actions that can be performed
        """
        pass

    def apply_action(self, player, action):
        """Applies the given action for the player on the current game board and returns a reward if there is any.

        Args:
            action (Action): an action to apply

        Returns:
            tuple(bool, int): a tuple with the first a boolean indicating whether the action was successfuly and the second a reward if the action was successfuly.
        """
        pass

    def serialize(self):
        """Serializes information about the current game board to a map of attritube with corresponding values.

        Returns:
            dict(X): a dictionary with attributes as key-value pairs
        """
        pass