from collections import deque
from Game.Common.i_state import IState
from Game.Common.action import Action


class MultiAgentState(IState):
    """
    A MultiAgentState is a combination of:
    -deque(str):
        a deque use as a circular queue to keep track of the turn of players, with the color string at first element of the queue representing the current turn player
    -IBoard:
        a board object containing all information about a game board
    -dict(str:int):
        a dictionary with player color as keys and their corresponding scores as values

    A MultiAgentState represents a board game state that consist of more than one players, keeping track of information about player turns and scores and the board as the game progresses with different player taking their turns to advance the state.
    
    A MultiAgentState implements the IState interface.
    """

    def __init__(self, players, board):
        """Initializes a multi agent game state by consuming the given players and board object. 

        Args:
            players (list(str)): a list of color string representing players in a game, with the order of players in the list as their initial turn order
            board (IBoard): a board object that contains all information on the board of the current game
        """
        self.turn_queue = deque(players, maxlen=len(players))
        self.board = board
        self.scores = self.initialize_scores()

    def initialize_scores(self):
        """Initializes the scores for all players in the game.
        """
        return {player:0 for player in self.turn_queue}

    def valid_actions(self):
        """Finds the list of valid action from the multi agent game state, returns false if there are no player in the current game state.

        Returns:
            union(list(Action), false): a list of actions or false if there are no players in the current game state
        """
        if self.turn_queue:
            return self.board.valid_actions(self.turn_queue[0])
        return False

    def apply_action(self, action):
        """Applies the given action to the game state.

        Args:
            action (Action): the game action to apply
        
        Returns:
            bool: a boolean with true representing the action is applied properly and the curent state advanced
        """
        if self.turn_queue:
            success, reward = self.board.apply_action(self.turn_queue[0], action)
            if success:
                self.scores[self.turn_queue[0]] += reward
                self.turn_queue.rotate(-1)
            return success
        return False

    def current_player(self):
        """Finds the player who's turn it is currently, returns false if there are no player in the curent game state.

        Returns:
            union(str, false): the color string representing the player or false meaning there are no players in the game
        """
        if self.turn_queue:
            return self.turn_queue[0]
        return False

    def game_over(self):
        """Check whether the game is over with the current game state.

        Returns:
            bool: a boolean with true representing that the game is over
        """
        if self.turn_queue:
            return self.board.game_over()
        return True

    def remove_player(self, player):
        """Removes the given player from the current game state.

        Args:
            player (str): the color string representing the player to kick

        Returns:
            bool: a boolean with true representing the player is removed properly
        """
        if player in self.turn_queue:
            del self.scores[player]
            self.turn_queue.remove(player)
            return self.board.remove_player(player)
        return False

    def game_score(self, player):
        """Finds the score of the given player in the current game, returns false if the player doesn't exist in the game.

        Args:
            player (str): the color string representing the player

        Returns:
            union(int, false): a non negative integer representing the score or false if palyer is not found
        """
        if player in self.scores:
            return self.scores[player]
        return False

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
        return {
            "players": [player for player in self.turn_queue],
            "scores": self.scores.copy(),
            "board": self.board.serialize()
        }