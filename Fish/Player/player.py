
import sys
sys.path.append('..')

from Fish.Common.state import GameState
from Fish.Common.game_tree import GameTree
from Fish.Common.message import Message

# A GamePlayer is a (Strategy, State, Color, GamePhase)
# The client will use this object to store information about the game state
# from the server. As it polls the data the client will check if it is the
# players turn. If so it will then send the server the players move or placement
# depending on the game phase.

DEFAULT_DEPTH = 2
class Player:


    # Initializes a player object with the strategy that they will be using
    # Strategy, Age -> Player
    def __init__(self, strategy, age, depth=DEFAULT_DEPTH, id=None):
        self.strategy = strategy
        self.state = None
        self.color = None
        self.gamephase = None
        self.age = age
        self.depth = depth
        self.id = id
        self.in_tournament = False
        self.winner = None

    # Returns the age of the player
    # Void -> Int
    def get_age(self):
        return self.age

    # Returns the id of the player
    # Void -> Str
    def get_id(self):
        return self.id

    # Updates the player's internal saved stated
    # GameState -> Void
    def set_state(self, state):
        self.state = GameState.generate_game_state(*state)
        return True

    # Assigns the player their color
    # Color -> Void
    def set_color(self, color):
        self.color = color
        return True

    # Updates the player's gamestate with the given placement action
    # Placement -> Void
    def perform_placement(self, placement):
        self.state.place_penguin(*placement)
        return True

    def perform_movement(self, movement):
        self.state.apply_move(movement)
        return True

    def kick_player(self, color):
        self.state.remove_player(color)
        return True

    # Gets the position of the players placement based on their strategy
    # Void -> Position
    def get_placement(self):
        return (self.color, self.strategy.get_placement(self.state))

    # Gets the move of the players placement based on their strategy
    # Void -> Move
    def get_move(self):
        return self.strategy.get_move(GameTree(self.state), self.depth)

    def tournamnent_started(self, content):
        self.in_tournament = True
        return True

    def recieve_results(self, result):
        self.winner = result
        self.in_tournament = False
        return True
        
    # Updates a players internal state based on the message from a referee
    # returns false if the player failed to recieve the message
    # Message -> Boolean
    def send_message(self, message):
        handler_table = {
            Message.COLOR_ASSIGNMENT: self.set_color,
            Message.PLACEMENT: self.perform_placement,
            Message.INITIAL_STATE: self.set_state,
            Message.MOVEMENT: self.perform_movement,
            Message.PLAYER_KICK: self.kick_player,
            Message.TOURNAMENT_START: self.tournamnent_started,
            Message.TOURNAMENT_RESULT: self.recieve_results
        }

        if message['type'] in handler_table:
            handler = handler_table[message['type']]
        else:
            return False

        try:
            result = handler(message['content'])
            return result
        except expression as identifier:
            return False
