from enum import Enum


class BoardType(Enum):
    """
    A BoardType is a enum that represents the type of available board implementations to play games on. When adding support for a new board implementation need to add the corresponding type here.
    """
    FISH = "fish"
    CHECKER = "checker"
    MARBLE = "marble"
    INVALID = "invalid"

    @classmethod
    def value2type(cls, value):
        """Determines the BoardType of the given board-type message.

        Args:
            value (string): a string as specified in the protocol message types

        Returns:
            BoardType.Type: a member of BoardType
        """
        for member in cls.__members__.values():
            if member.value == value:
                return member
        return cls.INVALID

    def is_valid(self):
        return self != self.INVALID

class IBoard:
    """
    An IBoard is the interface of board games, ensuring that all proper board implementations provides the essential function to find valid actions, apply a given action and provide a serialized copy of it's internal data representation.

    A Posn is a (Int, Int)
    It represents a 2D coordinate on a game board, where the first element is the row and the second the column positions, both row and column has to be greater or equal to 0.

    An Action is one of:
    - False: for a skip action
    - Posn: for placing a player avatar at a position
    - (Posn, Posn): for moving a player avatar from Posn one to another
    It represents an action that a player can take on the board.
    """
    
    def set_layout(self, layout):
        """Sets the layout of the board to the given one.

        Args:
            layout (2d list): 2d list of the board grid layout

        Returns:
            bool: a boolean with true indicating layout set successfully
        """
        pass

    def set_avatars(self, avatars):
        """Sets the avatars of the board to the given one.

        Args:
            avatars (dict): a dictionary with player color as keys and corresponding lists of Posn as the positions of avatars they have

        Returns:
            bool: a boolean with true indicating avatars set successfully
        """
        pass

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
            tuple(bool, int): a tuple with the first a boolean indicating whether the action was successful and the second a reward if the action was successfuly.
        """
        pass

    def remove_player(self, player):
        """Removes the given player from game board.

        Args:
            player (str): a color string representing a player

        Returns:
            bool: a boolean with true indicating the player was successfully removed
        """
        pass

    def game_over(self):
        """Determines if the game is over with the board state.

        Returns:
            bool: a boolean with true indicating the game is over
        """
        pass

    def serialize(self):
        """Serializes information about the current game board to a dict of attritube with corresponding values.

        Returns:
            dict(X): a dictionary with attributes as key-value pairs
        """
        pass
