from enum import Enum


class ActionType(Enum):
    """
    A ActionType is a enum that represents the type of available actions in a game.
    """
    SKIP = "skip"
    PLACEMENT = "placement"
    MOVEMENT = "movement"
    INVALID = "invalid"

    def is_valid(self):
        return self != self.INVALID

class Action:
    """
    Action is a static class that encapulates functionality to determine the type of action given a value.

    An Action is one of:
    -skip: 
        a string that represents a skip action with the ActionType of SKIP
    
    -placement: 
        a Posn that represents placing a player avatar at a board position with the ActionType of PLACEMENT

    -movement:
        a tuple(Posn,Posn) that represents moving a player avatar from one position to another on the board with ActionType of MOVEMENT, where the first is the position to move from and the second to

    A Posn is a tuple(Int, Int)
    It represents a 2D coordinate on a game board, where the first element is the row and the second the column positions, both row and column has to be greater or equal to 0.
    """

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
                    return ActionType.PLACEMENT
                elif Action.is_posn(*action[0]) and Action.is_posn(*action[1]):
                    return ActionType.MOVEMENT
            elif action == ActionType.SKIP.value:
                return ActionType.SKIP
            else:
                return ActionType.INVALID
        except Exception as _:
            return ActionType.INVALID

    @staticmethod
    def is_posn(r, c):
        return isinstance(r, int) \
                and isinstance(c, int) \
                and r >= 0 \
                and c >= 0

