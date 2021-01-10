class Action:
    """
    An Action is one of:
    - False: for a skip action
    - Posn: for placing a player avatar at a position
    - (Posn, Posn): for moving a player avatar from Posn one to another
    
    It represents an action that a player can take on the board.

    An ActionType is one of:
    -SKIP: if the action is false
    -PLACEMENT: if the action is a Posn
    -MOVEMENT: if the action is a tuple of Posn
    -INVALID: otherwise

    A Posn is a (Int, Int)
    It represents a 2D coordinate on a game board, where the first element is the row and the second the column positions, both row and column has to be greater or equal to 0.
    """

    SKIP = "skip"
    PLACEMENT = "placement"
    MOVEMENT = "movement"
    INVALID = "invalid"

    @staticmethod
    def type(action):
        """Determines the type of the given action as either, skip action, placement action, movement action or an invalid one.

        Args:
            action (Action): an action to find the type

        Returns:
            ActionType: the type of action
        """
        try:
            length = len(action)
            if length == 2:
                if Action.is_posn(*action):
                    return Action.PLACEMENT
                elif Action.is_posn(*action[0]) and Action.is_posn(*action[1]):
                    return Action.MOVEMENT
            elif action == Action.SKIP:
                return Action.SKIP
            else:
                return Action.INVALID
        except Exception as _:
            return Action.INVALID

    @staticmethod
    def is_posn(r, c):
        return isinstance(r, int) \
                and isinstance(c, int) \
                and r >= 0 \
                and c >= 0

