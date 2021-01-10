from Game.Player.Strategies.minimax_strategy import MinimaxStrategy
from Game.Player.i_player import IPlayer
from Game.Common.i_state import IState

class MinimaxPlayer(IPlayer):
    """
    An MinimaxPlayer is a union of:
    -IStrategy:
        a strategy object that the player used to find the best action
    -IState:
        a game state of the board game

    An MinimaxPlayer represents a AI player developed internally for example purposes. This implementation is a stateful one leveraging the updates it gets for being an observer and uses the minimax strategy when finding best action to take.

    The MinimaxPlayer implements the IPlayer interface.
    """

    def __init__(self, depth=2, id=None):
        """Initializes a AI player that uses the minimax strategy to find the best action in a board game.

        Args:
            depth (int, optional): a positive integer to set how deep to search with the minimax strategy. Defaults to 2.
            id (int, optional): a non negative integer uniquely identifies a player in the system. Defaults to None.
        """
        self.id = id
        self.state = None
        self.strategy = self.generate_strategy(depth)

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
        return self.strategy.get_action(self.state)

    def generate_strategy(self, depth):
        """Generate and returns a minimax strategy set to search at the given depth and uses the internal state evaluation function.

        Args:
            depth (int): a postive integer

        Returns:
            IStrategy: a strategy object
        """
        return MinimaxStrategy(self.evaluate_state, depth)


    def evaluate_state(self, player, game_state):
        """Evaluates the value of a state for the specified player.

        Args:
            player (str): a color string representing a player
            game_state (int): a non negative integer
        """
        score = game_state.game_score(player)
        if score:
            return score 
        return 0