from Common.state import GameState
from Common.game_tree import GameTree

# A GamePlayer is a (Strategy, State, Color, GamePhase)
# The client will use this object to store information about the game state
# from the server. As it polls the data the client will check if it is the
# players turn. If so it will then send the server the players move or placement
# depending on the game phase.
class Player:

    DEPTH = 2

    # Initializes a player object with the strategy that they will be using
    # Strategy, Age -> Player
    def __init__(self, strategy, age):
        self.strategy = strategy
        self.state = None
        self.color = None
        self.gamephase = None
        self.age = age

    # Returns the age of the players
    # Void -> Int
    def get_age(self):
        return self.age

    # Updates the player's internal saved stated
    # GameState -> Void
    def set_state(self, state):
        self.state = GameState.generate_game_state(*state)

    # Assigns the player their color
    # Color -> Void
    def set_color(self, color):
        self.color = color

    # Gets the position of the players placement based on their strategy
    # Void -> Position
    def get_placement(self):
        if self.state is None:
            raise ValueError("state is not set")

        return self.strategy.get_placement(self.state)

    # Gets the move of the players placement based on their strategy
    # Void -> Move
    def get_move(self):
        if self.state is None:
            raise ValueError("state is not set")

        return self.strategy.get_move(GameTree(self.state), self.DEPTH)
