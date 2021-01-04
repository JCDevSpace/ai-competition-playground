import copy

from Game.Common.i_state import IState


class SingleAgentState(IState):
    """
    A SingleAgentState is a union of:
    -str:
        a color string representing the current player of the single agent board game
    -IBoard:
        a board object that implements the board interface representing one of the available single agent game boards
    -int:
        a positive integer representing the current score of the player

    A SingleAgentState represents a board game state that consist of only one player, keeping track of information about the color the player is playing as, the score the player has, and the board as the game progresses with the player taking actions to advance the state.
    """

    def __init__(self, player, board):
        """Initializes a single agent game state with the given player and board object.

        Args:
            player (str): a color string representing the player
            board (IBoard): a board object that contains all information on the board of the curent game
        """
        self.player = player
        self.board = copy.deepcopy(board)
        self.score = 0

    def valid_actions(self):
        """Finds the list of valid action from the current game state.

        Returns:
            List(IAction): a list of actions
        """
        pass


    def apply_action(self, player, action):
        """Applies the given action to the current game state for the given player.

        Args:
            player (str): a color string representing a player
            action (IAction): the game action to apply
        
        Returns:
            bool: a boolean with true representing the action is applied properly and the curent state advanced, and false for atemtping to apply an invalid action or not the current player's turn
        """
        pass

    def current_player(self):
        """Finds the player who's turn it is currently.

        Returns:
            str: the color string representing the player
        """
        pass

    def game_over(self):
        """Check whether the game is over with the current game state.

        Returns:
            bool: a boolean with true representing that the game is over and false not
        """
        pass

    def remove_player(self, player):
        """Removes the given player from the current game state.

        Args:
            player (str): the color string representing the player to kick

        Returns:
            bool: a boolean with true representing the player is removed properly and false not
        """
        pass

    def game_winners(self):
        """Finds the winner of the game if the game is over, required to check whether the game is over first.

        Returns:
            list(str): a list of strings with each element representing a winner's unique color string 
        """
        pass

    def serialized(self):
        """Serializes information that represents the current game state into a map of attribute with corresponding values.

        Returns:
            dict(x): a dictionary with important attributes as key-value pairs
        """
        pass