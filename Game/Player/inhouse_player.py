from Game.Player.i_player import IPlayer


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
        """Initializes a AI player that uses a specific strategy to find the best action in a board game.

        Args:
            strategy (IStrategy): a strategy object to use when finding the best action to take 
            id (int, optional): a non negative integer uniquely identifies a player in the system. Defaults to None.
        """
        self.strategy = strategy

        self.state = None

    def game_start_update(self, players, game_info):
        """Updates the observer on the start of a board game with the starting players and the game information.

        Args:
            players (list(str)): a list of color string
            game_info (dict): a dict contain all information about a game
        """
        pass

    def game_action_update(self, action):
        """Updates the observer on an action progress of a board game.

        Args:
            action (Action): an action
        """
        pass

    def game_kick_update(self, player):
        """Updates the observer on a player kick from the board game.

        Args:
            player (str): a color string representing a player
        """
        pass
    
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
        pass

    def playing_with(self, colors):
        """Updates the player the other colors that it's playing against.

        Args:
            colors (list(str)): a list of color string
        """
        pass

    def get_action(self, game_state):
        """Finds the action to take in a board game given the current game state, the player also recieves all action and player kick updates due to being an observer, thus a stateful implementation is also viable.

        Args

        Returns:
            Action: an action to take
        """
        pass


    # Updates the player of the initial state of the game
    # returns True if the update was successfully processed
    # else False
    # Serialized GameState -> Boolean
    def inital_state_update(self, state):
        self.state = GameState.generate_game_state(*state)
        return True

    # Updates the player on it's color assignment in the game
    # returns True if the update was successfully processed
    # else False
    # Color -> Boolean
    def color_assignment_update(self, color):
        self.color = color
        return True

    # Updates the player of a placement action in the game
    # returns True if the update was successfully processed
    # else False
    # Placement -> Boolean
    def placement_update(self, placement):
        self.state.place_penguin(*placement)
        return True

    # Updates the player of a movement action in the game
    # returns True if the update was successfully processed
    # else False
    # Move -> Boolean
    def movement_update(self, movement):
        self.state.apply_move(movement)
        return True

    # Updates the player of a player kick in the game
    # returns True if the update was successfully processed
    # else False
    # Kick -> Boolean
    def player_kick_update(self, kick):
        if kick[0] == self.color:
            self.kicked = True
        self.state.remove_player(kick[0])
        return True

    # Gets a placement action from the player
    # Void -> Placement
    def get_placement(self):
        return (self.color, self.strategy.get_placement(self.state))

    # Gets a movement action from the player
    # Void -> Move
    def get_move(self):
        result = self.strategy.get_move(GameTree(self.state), self.depth)
        return result

    # Updates the player on the start of a tournament
    # returns True if the update was successfully processed
    # else False
    # Any -> Boolean
    def tournamnent_start_update(self):
        self.in_tournament = True
        self.kicked = False
        return True

    # Updates the player whether they have won the tournament
    # returns True if the update was successfully processed
    # else False
    # Boolean -> Boolean
    def tournamnent_result_update(self, won):
        self.won = won
        self.in_tournament = False
        return True
