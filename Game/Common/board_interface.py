class IBoard:
    """A IBoard represents the board of a board game, keeping track of board dimensions, board configuration/arrangement and game pieces on the board.
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
        """Finds the list of valid position to move to for the given starting position.

        Args:
            from_posn (Posn): a position to start from

        Returns:
            list(Posn): a list of board positions
        """
        pass

    def serialize(self):
        """Serializes information about the current game board to a map of attritube with corresponding values.

        Returns:
            dict(X): a dictionary with attributes as key-value pairs
        """
        pass