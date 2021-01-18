from Game.Common.util import safe_execution, load_config
import Game.Admin.game_builder as GameBuilder
from copy import deepcopy


class Referee:
    """
    A Referee is a combination of:
    -IState:
        a game state of the running board game
    -dict(str:IPlayer):
        a dict of color string to player object, where the str represents the color that the corresponding player is assigned with in the game
    -list(IObsever):
        a list of observer objects to inform changes to the game
    -list(str):
        a list of color string representing all kicked players

    A Referee controls the creation and running of board games, handling interaction to and from both players and observers. Taking responsibility to inform all observers on game progresses and asking players to take move when it's their turn, as well as kicking any player for abnormal interactions.

    Abnormal interactions here includes failure to respond to action request due to either timeout or crashing.

    The Referee initializes games based on configurations loaded from the some of the configuration files.
    """

    def __init__(self, game_config, players, observers=None):
        """Initializes a referee with the given players and observers, the referee performs some of the initialization base on the corresponding configuration files.

        Args:
            game_type (str): a string representing the type of game the referee will initialize
            players (list(IPlayer)): a list of player object
            observers (list(IObserver), optional): a list of observer object. Defaults to None.
        """
        print("Referee got config", game_config)
        ref_config = load_config("default_referee.yaml")

        self.interaction_timeout = ref_config["interaction_timeout"]

        turn_order = self.assign_colors(players, game_config["config"]["player_colors"])
        
        if observers:
            self.observers = observers
        else:
            self.observers = []

        self.kicked_players = []

        
        state = GameBuilder.state_from_config(turn_order, game_config)
        if not state:
            raise RuntimeError("Failed to build game from configuration")
        self.game_state = state

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

    def run_game(self):
        """Runs the game to completion, updating all player and observers on game progresses and returns the final winners and everyone who got kicked once the game is over.

        Returns:
            tuple(list(IPlayers)): a tuple of list of player objects, where the first is the list of winner and the second the list of player who got kicked
        """
        self.inform_color_assignments()
        self.inform_game_start()

        while not self.game_state.game_over():
            self.run_turn()
        
        return self.game_results()

    def run_turn(self):
        """Runs one turn of the perform, a turn include asking the current player for an action, attempts to perform the action, informs everyone on the action if it was successfully performed or kicks the player if it was not.
        """
        player_color = self.game_state.current_player()
        player = self.players_dict[player_color]

        action, exc = safe_execution(player.get_action, [deepcopy(self.game_state)], wait=True, timeout=self.interaction_timeout)
        if not exc:
            success = self.game_state.apply_action(action)
            if success:
                self.inform_action(action)
                return
        self.kick_player(player_color)

    def inform_color_assignments(self):
        """Informs all players of their color assignment in the game.
        """
        for color, player in self.players_dict.items():
            safe_execution(player.playing_as, [color])

    def inform_game_start(self):
        """Informs all players and observers on the start of the game.
        """
        for color, player in self.players_dict.items():
            if color not in self.kicked_players:
                safe_execution(player.game_start_update, [deepcopy(self.game_state)])
        
        for observers in self.observers:
            safe_execution(observers.game_start_update, [deepcopy(self.game_state)])

    def inform_action(self, action):
        """Informs all players and observers on an action in the game.
        """
        for color, player in self.players_dict.items():
            if color not in self.kicked_players:
                safe_execution(player.game_action_update, [action])
        
        for observers in self.observers:
            safe_execution(observers.game_action_update, [action])

    def kick_player(self, player_color):
        """Kicks the given player from the game, removing him from the game state.

        Args:
            player_color (str): a color string representing a player
        """
        self.kicked_players.append(player_color)
        self.game_state.remove_player(player_color)
        self.inform_kick(player_color)

    def inform_kick(self, kick_color):
        """Informs all players and observers on a player kick, kicked player don't get the informed.

        Args:
            player_color (str): a color string representing a player
        """
        for color, player in self.players_dict.items():
            if color not in self.kicked_players:
                safe_execution(player.game_kick_update, [kick_color])
        
        for observers in self.observers:
            safe_execution(observers.game_kick_update, [kick_color])

    def game_results(self):
        """Finds the players who won and the players who got kicked.

        Returns:
            tuple(list): a tuple of lists with the first being the list of winners and the second players who got kicked
        """
        if len(self.kicked_players) != len(self.players_dict):
            final_scores = {color:self.game_state.game_score(color) for color in self.players_dict if color not in self.kicked_players}

            highest_score = max(final_scores.values())

            winners = [self.players_dict[color] for color, score in final_scores.items() if score == highest_score]            
        else:
            winners = []

        kicked_player = [player for color, player in self.players_dict.items() if color in self.kicked_players]
        
        return winners, kicked_player