from Game.Common.i_state import IState
from Game.Common.action import Action


class SingleAgentState(IState):
    """
    A SingleAgentState is a union of:
    -str:
        a color string representing the current player of the single agent board game
    -BoardBuilder:
        a builder object that handle building a board for the game state
    -int:
        a positive integer representing the current score of the player

    A SingleAgentState represents a board game state that consist of only one player, keeping track of information about the color the player is playing as, the score the player has, and the board as the game progresses with the player taking actions to advance the state.
    """

    def __init__(self, player, board_builder):
        """Initializes a single agent game state with the given player and board object.

        Args:
            player (str): a color string representing the player
            board (IBoard): a board object that contains all information on the board of the curent game
        """
        self.player = player
        self.board = board_builder.build()
        self.score = 0

    def valid_actions(self):
        """Finds the list of valid action from the single agent game state, returns false if there are no player in the current game state.

        Returns:
            union(list(Action), false): a list of actions or false if there are no players in the current game state
        """
        if self.player:
            return self.board.valid_actions(self.player)
        return False

    def apply_action(self, action):
        """Applies the given action to the current game state.

        Args:
            action (Action): the game action to apply
        
        Returns:
            bool: a boolean with true representing the action is applied properly and the curent state advanced
        """
        if self.player:
            success, reward = self.board.apply_action(self.player, action)
            if success:
                self.score += reward
            return success
        return False

    def current_player(self):
        """Finds the player who's turn it is currently, returns false if there are no player in the curent game state.

        Returns:
            union(str, false): the color string representing the player or false meaning there are no players in the game
        """
        if self.player:
            self.player
        return False

    def game_over(self):
        """Check whether the game is over with the current game state.

        Returns:
            bool: a boolean with true representing that the game is over
        """
        if self.player:
            return self.board.game_over()
        return True

    def remove_player(self, player):
        """Removes the given player from the current game state.

        Args:
            player (str): the color string representing the player to kick

        Returns:
            bool: a boolean with true representing the player is removed properly
        """
        if player == self.player:
            self.player = None
            return True
        return False

    def game_score(self, player):
        """Finds the score of the given player in the current game, returns false if the player doesn't exist in the game.

        Args:
            player (str): the color string representing the player

        Returns:
            union(int, false): a non negative integer representing the score or false if palyer is not found
        """
        if player == self.player:
            return self.score
        return False

    def serialized(self):
        """Serializes information that represents the current game state into a map of attribute specified in the data representation.

        Returns:
            dict(x): a dictionary with important attributes as key-value pairs in the following format:
            {   
                "players": list(str),
                "scores": dict(str:int),
                "board": IBoard.serialize()
            }
        """
        return {
            "players": [self.player],
            "scores": {self.player:self.score},
            "board": self.board.serialize()
        }