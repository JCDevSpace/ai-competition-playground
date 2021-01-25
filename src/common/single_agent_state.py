from src.common.i_state import IState, StateType


class SingleAgentState(IState):
    """
    A SingleAgentState is a combination of:
    -str:
        a color string representing the current player of the single agent board game
    -IBoard:
        a board object containing all information about the game board
    -int:
        a positive integer representing the current score of the player

    A SingleAgentState represents a board game state that consist of only one player, keeping track of information about the color the player is playing as, the score the player has, and the board as the game progresses with the player taking actions to advance the state.
    """

    def __init__(self, player, board):
        """Initializes a single agent game state by consuming the given player and board object.

        Args:
            player (str): a color string representing the player
            board (IBoard): a board object that contains all information on the board of the curent game
        """
        self.player = player
        self.board = board
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
            return self.player
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

    def set_score(self, player, score):
        """Set the score of the given player.

        Args:
            player (str): a color string
            score (int): a non-negative integer
        
        Returns:
            bool: a boolean with true indicating set successfully
        """
        if player == self.player:
            self.score = score
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

    def game_winners(self):
        """Find the winners of the game base on the current state, only works when the game is already over.

        Returns:
            union(list, False): a list of player color or False
        """
        if self.game_over():
            #temporary place holder
            return [self.player] if self.score >= 15 else []
        return False

    def serialize(self):
        """Serializes information that represents the current game state into a map of attribute specified in the data representation.

        Returns:
            dict(x): a dictionary with important attributes as key-value pairs in the following format:
            {   
                "state-type": StateType.value
                "info": {
                    "players": list(str),
                    "scores": dict(str:int),
                    "board": IBoard.serialize()
                }
            }
        """
        return {
            "state-type": StateType.SINGLEAGENT.value,
            "info": {
                "players": [self.player],
                "scores": {self.player:self.score},
                "board": self.board.serialize()
            }
        }