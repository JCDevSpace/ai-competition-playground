import yaml
from copy import deepcopy
from Game.Common.util import safe_execution


class Referee:
    """
    A Referee is a union of:
    -IState:
        a game state of the running board game
    -dict(str:IPlayer):
        a dict of color string to player object, where the str represents the color that the corresponding player is assigned with in the game
    -list(IObsever):
        a list of observer objects to update game the game
    -list(str):
        a list of color string representing all kicked players

    A Referee controls the creation and running of board games, handling interaction to and from both players and observers. Taking responsibility to update all observers on game progresses and asking players to take move when it's their turn, as well as kicking any player for abnormal interactions.

    Abnormal interactions here includes failure to respond to action request due to either timeout or crashing.

    The Referee initializes games based on configurations loaded from the some of the configuration files.
    """

    CONFIG_PATH = "../../configs/"

    def __init__(self, game_type, players, observer=None):
        """Initializes a referee with the given players and observers, the referee performs some of the initialization base on the corresponding configuration files.

        Args:
            game_type (str): a string representing the type of game the referee will initialize
            players (list(IPlayer)): a list of player object
            observer (list(IObserver), optional): a list of observer object. Defaults to None.
        """
        ref_config = self.load_config("default_referee.yaml")

        self.interaction_timeout = ref_config["interaction_timeout"]

        game_config = self.load_config(ref_config[game_type])

        turn_order = self.assign_colors(players, game_config["player_colors"])
        
        if observer:
            self.observer = observer
        else:
            self.observer = []

        self.kicked_players = []

        self.game_state = self.initialize_game_state(turn_order, game_config)

    def load_config(self, config_file):
        """Loads the configuration from the given yaml file and returns it as a dictionary of configurations.

        Args:
            config_file (str): a str of the yaml file

        Returns:
            dict: a dictionary of the configuration
        """
        with open(self.CONFIG_PATH + config_file) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def assign_colors(self, players, colors):
        """Assigns color to players by consuming the given list of players and available player colors then, returns the turn order of the player colors after assignment.

        Args:
            players (list(IPlayer)): a list of player objects
            colors (list(str)): a list of color string

        Returns:
            dict(str:IPlayer): a dictionary
        """
        self.players_dict = {}
        turn_order = []

        for i, player in enumerate(players):
            self.players_dict[colors[i]] = player
            turn_order.append(colors[i])

        return turn_order

    def initialize_game_state(self, turn_order, game_config):
        """Initializes a game state with the given turn order and game configuration.

        Args:
            turn_order (list(str)): a list of color string
            game_config (dict): a dictionary of game configurations

        Returns:
            IState: a game state
        """
        pass

    def run_game(self):
        """Runs the game to completion, updating all player and observer on game progresses and returns the final winners and everyone who got kicked once the game is over.

        Returns:
            tuple(list(IPlayers)): a tuple of list of player objects, where the first is the list of winner and the second the list of player who got kicked
        """
        self.update_color_assignments()
        self.update_game_start()

        while not self.game_state.game_over():
            self.run_turn()

        return False

    def run_turn(self):
        """Runs one turn of the perform, a turn include asking the current player for an action, attempts to perform the action, updates everyone on the action if it was successfully performed or kicks the player if it was not.
        """
        player_color = self.game_state.current_player()
        player = self.players_dict[player_color]

        action, exc = safe_execution(player.get_action(deepcopy(self.game_state)), timeout=self.interaction_timeout)
        if not exc:
            success = self.game_state.apply_action(action)
            if success:
                self.update_action(action)
        self.kick_player(player_color)

    def update_color_assignments(self):
        """Updates all players of their color assignment in the game.

        Returns:
            bool: a boolean with true indicating all players were successfully updated on their color assignment
        """
        for color, player in self.players_dict.items():
            safe_execution(player.playing_as(color), timeout=self.interaction_timeout)
        return True

    def update_game_start(self):
        """Updates all players and observers on the start of the game.

        Returns:
            bool: a boolean with true indicating all players and observers were updated successfully
        """
        for color, player in self.players_dict.items():
            if color not in self.kicked_players:
                safe_execution(player.game_start_update(deepcopy(self.game_state)), timeout=self.interaction_timeout)
        
        for observer in self.observer:
            safe_execution(observer.game_start_update(deepcopy(self.game_state)), timeout=self.interaction_timeout)

        return True

    def update_action(self, action):
        """Updates all players and observers on an action in the game.

        Returns:
            bool: a boolean with true indicating all players and observers were updated successfully
        """
        for color, player in self.players_dict.items():
            if color not in self.kicked_players:
                safe_execution(player.game_action_update(action), timeout=self.interaction_timeout)
        
        for observer in self.observer:
            safe_execution(observer.game_action_update(action), timeout=self.interaction_timeout)

        return True

    def kick_player(self, player_color):
        """Kicks the given player from the game, removing him from the game state.

        Args:
            player_color (str): a color string representing a player

        Returns:
            bool: a boolean with true indicating the player was successfully kicked
        """
        self.kicked_players.append(player_color)
        self.game_state.remove_player(player_color)
        self.update_kick(player_color)
        return True

    def update_kick(self, kick_color):
        """Updates all players and observers on a player kick, kicked player don't get the update.

        Args:
            player_color (str): a color string representing a player

        Returns:
            bool: a boolean with true indicating all players and observers are updated successfully on the player kick
        """
        for color, player in self.players_dict.items():
            if color not in self.kicked_players:
                safe_execution(player.game_kick_update(kick_color), timeout=self.interaction_timeout)
        
        for observer in self.observer:
            safe_execution(observer.game_kick_update(kick_color), timeout=self.interaction_timeout)

        return True