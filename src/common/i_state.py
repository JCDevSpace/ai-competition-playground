from copy import deepcopy
from enum import Enum


class StateType(Enum):
    """
    A StateType is a enum that represents the type of available state implementations to run games with. When adding support for a new state implementation need to add the corresponding type here.
    """
    MULTIAGENT = "multi-agent"
    SINGLEAGENT = "single-agent"
    INVALID = "invalid"

    @classmethod
    def value2type(cls, value):
        """Determines the BoardType of the given state-type message.

        Args:
            value (string): a string as specified in the protocol message types

        Returns:
            StateType.Type: a member of StateType
        """
        for member in cls.__members__.values():
            if member.value == value:
                return member
        return cls.INVALID

    def is_valid(self):
        return self != self.INVALID

class IState:
    """
    An IState is the interface for the state of board games, ensuring all proper implementations of the state provide the essential functionality to find all valid actions, applying a given action, find the current player, kick a player, determin if a game is over, finding the winners if it is and provide serialized copies of it's internal data representation.
    """

    def successor_state(self, action):
        """Generates the new successor state from the result of applying the given action from the current state.

        Args:
            action (Action): an action

        Returns:
            union(IState, false): a new IState or false if the action can't be successfully applied to the state of the current node.
        """
        state_copy = deepcopy(self)
        
        if state_copy.apply_action(action):
            return state_copy
        return False

    def set_score(self, player, score):
        """Set the score of the given player.

        Args:
            player (str): a color string
            score (int): a non-negative integer
        
        Returns:
            bool: a boolean with true indicating set successfully
        """
        pass

    def valid_actions(self):
        """Finds the list of valid action from the current game state, returns false if there are no player in the current game state.

        Returns:
            union(list(Action), false): a list of actions or false if there are no players in the current game state.
        """
        pass

    def apply_action(self, action):
        """Applies the given action to the game state.

        Args:
            action (IAction): the game action to apply
        
        Returns:
            bool: a boolean with true representing the action is applied properly and the curent state advanced
        """
        pass

    def current_player(self):
        """Finds the player who's turn it is currently, returns false if there are no player in the curent game state.

        Returns:
            union(str, false): the color string representing the player or false meaning there are no players in the game
        """
        pass

    def game_over(self):
        """Check whether the game is over with the current game state.

        Returns:
            bool: a boolean with true representing that the game is over
        """
        pass

    def remove_player(self, player):
        """Removes the given player from the current game state.

        Args:
            player (str): the color string representing the player to kick

        Returns:
            bool: a boolean with true representing the player is removed properly
        """
        pass

    def game_score(self, player):
        """Finds the score of the given player in the current game,returns false if the player doesn't exist in the game.

        Args:
            player (str): the color string representing the player

        Returns:
            union(int, false): a non negative integer representing the score or false if palyer is not found
        """
        pass

    def game_winners(self):
        """Find the winners of the game base on the current state, only works when the game is already over.

        Returns:
            union(list, False): a list of player color or False
        """
        pass

    def serialize(self):
        """Serializes information that represents the current game state into a map of attribute with corresponding values.

        Returns:
            dict(x): a dictionary with important attributes as key-value pairs in the following format:
            {   
                "players": list(str),
                "scores": dict(str:int),
                "board": IBoard.serialize()
            }
        """
        pass