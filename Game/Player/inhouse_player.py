from Game.Player.i_player import IPlayer
from Game.Common.i_state import IState

class InhousePlayer(IPlayer):
    """
    An InhousePlayer is a union of:
    -IStrategy:
        a strategy object that the player used to find the best action
    -IState:
        a game state of the board game

    An InhousePlayer represents a AI player developed internally for example purposes, different strategies can be swapped as needed. This implementation is a stateful one leveraging the updates it gets for being an observer.

    The InHousePlayer implements the IPlayer interface.
    """

    def __init__(self, strategy, id=None):
        """Initializes a AI player that uses the given strategy to find the best action in a board game.

        Args:
            strategy (IStrategy): a strategy object to use when finding the best action to take 
            id (int, optional): a non negative integer uniquely identifies a player in the system. Defaults to None.
        """
        self.strategy = strategy
        self.state = None

        self.id = id

    def get_id(self):
        if self.id:
            return self.id
        return False

    def game_start_update(self, game_state):
        """Updates the observer on the start of a board game by consuming the given starting players and the game state.

        Args:
            game_state (IState): a game state object
        """
        if not self.state:
            self.state = game_state

    def game_action_update(self, action):
        """Updates the observer on an action progress of a board game.

        Args:
            action (Action): an action
        """
        if self.state:
            self.state.apply_action(action) 

    def game_kick_update(self, player):
        """Updates the observer on a player kick from the board game.

        Args:
            player (str): a color string representing a player
        """
        if self.state:
            self.state.remove_player(player)
    
    def tournament_start_update(self, players):
        """Updatest the observer on the start of a board game tournament with the initial contestents.

        Args:
            players (list(str)): a list of color string
        """
        pass

    def tournament_progress_update(self, advanced_players, knocked_players):
        """Updates the observer on the progress of a board game tournament with players who advanced to the next round and the players who got knocked out.

        Args:
            advanced_players (list(str)): a list of color string
            knocked_players (list(str)): a list of color string
        """
        pass

    def tournament_end_update(self, winners):
        """Updates the observer on the final winners of the board game tournament, the finals winners include the top three players, with first player in the winners list as first place and the last one as thrid place. 

        Args:
            winners (list(str)): a list of color string
        """
        pass

    def playing_as(self, color):
        """Updates the player the color that it's playing as in a board game.

        Args:
            color (str): a color string
        """
        self.color = color

    def get_action(self, game_state):
        """Finds the action to take in a board game by consuming the given game state, the player also recieves all action and player kick updates due to being an observer, thus a stateful implementation is also viable.

        Args:
            game_state (IState): a game state object

        Returns:
            Action: an action to take
        """
        self.strategy.get_action(self.state)
