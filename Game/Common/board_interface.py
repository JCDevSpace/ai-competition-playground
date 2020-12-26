class IBoard:
    """A IBoard represents the board of a board game, keeping track of board dimensions, board configuration/arrangement and game piece positions on the board.

    A Posn is a (Int, Int)
    It represents a 2D coordinate on a game board, where the first element is the row and the second the column positions, both row and column has to be greater or equal to 0.
    """

    def valid_from_position(self, player):
        """Finds the list of valid position for the given player to pick from.

        Args:
            player (str): a color string representing a player

        Returns:
            list(Posn): a list board positions
        """
        pass

    def reachable_positions(self, from_posn):
        """Finds the list of reachable positions from the given starting position.

        Args:
            from_posn (Posn): a position to start from

        Returns:
            list(Posn): a list of board positions
        """
        pass

    def reward(self, from_posn, to_posn):
        """Find the reward of making a move from the given from position to the given to position.

        Args:
            from_posn (Posn): a position to moved from
            to_posn (Posn): a position to moved to

        Returns:
            int: a non-negative integer reward value
        """
        pass

    def serialize(self):
        """Serializes information about the current game board to a map of attritube with corresponding values.

        Returns:
            dict(X): a dictionary with attributes as key-value pairs
        """
        pass