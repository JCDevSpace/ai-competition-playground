# A GamePhase is one of
# - "waiting"
# - "placement"
# - "playing"
# - "finished"
# This represents what part of the game is happening at a given moment

# This class handles the communications between a player and referee
class PlayerInterface:

    # Returns a string representing the current GamePhase
    # Void -> GamePhase
    def get_game_phase():
        pass

    # While in the "waiting" GamePhase
    # returns how an integer represting the number of seconds until the game starts
    # 0 if in other game phases
    # Void -> int
    def time_until_start():
        pass

    # While in anyphase of the game returns a list of the other players in the lobby
    # Void -> List[Player]
    def get_players():
        pass

    # If the GamePhase is "placement" or "playing"
    # Returns true if it the players turn in the given phase of the game
    # Void -> Boolean
    def my_turn_huh():
        pass

    # If the GamePhase is "placement", "playing", or "finished"
    # Returns the current GameState from the referee
    # Void -> GameState
    def get_game_state():
        pass

    # If the GamePhase is "placement" and it is the calling players turn,
    # Asks referee to place a penguin at the given position
    # Returns True if successful, if unsuccessful returns False
    # the player is kicked
    # Position -> Booleans
    def place_penguin(posn):
        pass

    # If the GamePhase is "playing" and it is the calling players turn,
    # it asks referee to move a penguin
    # Returns True if successful, if unsuccessful returns False
    # the player is kicked
    # Move -> Boolean
    def make_move(move):
        pass

    # If the GamePhase is "playing" and it is the calling players turn
    # then this returns a list of that player's valid moves
    def get_my_valid_moves():
        pass

    # If the GamePhase is "playing" and it is the calling players turn
    # Asks the referee what the game state would be after applying a certain move
    # Returns false if the player would get kicked for this action
    # Move -> GameState or False
    def query_move(move):
        pass

    # If the GamePhase is "finished" then it
    # returns True, returns False otherwise
    # Void -> Boolean
    def game_over_huh():
        pass

    # If the GamePhase is "finished" then it
    # asks the referee who the color of the winner is
    # Void -> Color
    def get_winner():
        pass

    # asks the referee what the calling player's color is
    # Void -> Color
    def get_my_color():
        pass

    # Kicks the calling player from the game in any phase
    # Void -> Void
    def quit():
        pass
