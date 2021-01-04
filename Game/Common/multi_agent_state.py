import copy

from Game.Common.i_state import IState


class MultiAgentState(IState):
    """
    A MultiAgentState is a union of:
    -deque(str):
        a deque use as a queue to keep track of the turn of players, with the color string at the front of the queue representing the current turn player
    -IBoard:
        a board object that implements the board interface representing one of the available multi agent game boards
    -dict(str:int):
        a dictionary with player color as keys and their corresponding scores as values

    A MultiAgentState represents a board game state that consist of more than one players, keeping track of information about player turns and scores and the board as the game progresses with different player taking their turns to advance the state.
    
    A MultiAgentState implements the IState interface.
    """

    def __init__(self, players, board):
        """Initializes a multi agent game state with the given players and board object. 

        Args:
            players (list(str)): a list of color string representing players in a game
            board (IBoard): a board object that contains all information on the board of the current game
        """
        self.players = copy.deepcopy(players)
        self.board = copy.deepcopy(board)
        self.scores = self.initialize_scores()

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
            action (Action): the game action to apply
        
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