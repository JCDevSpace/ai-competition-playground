# A GamePhase is one of
# - "waiting"
# - "placement"
# - "playing"
# - "finished"
# This represents what part of the game is happening at a given moment

# This class handles the communications between a player and referee
class PlayerInterface:
    # Returns the age of the player
    # Void -> Int
    def get_age(self):
        pass

    # Returns the id of the player
    # Void -> Str
    def get_id(self):
        pass

    # Returns the color that the player got assigned with in a game
    # Void -> Str
    def assigned_color(self):
        pass

    # Updates the player of the initial state of the game
    # returns True if the update was successfully processed
    # else False
    # Serialized GameState -> Boolean
    def inital_state_update(self, state):
        pass

    # Updates the player on it's color assignment in the game
    # returns True if the update was successfully processed
    # else False
    # Color -> Boolean
    def color_assignment_update(self, color):
        pass

    # Updates the player of a placement action in the game
    # returns True if the update was successfully processed
    # else False
    # Placement -> Boolean
    def placement_update(self, placement):
        pass

    # Updates the player of a movement action in the game
    # returns True if the update was successfully processed
    # else False
    # Move -> Boolean
    def movement_update(self, movement):
        pass

    # Updates the player of a player kick in the game
    # returns True if the update was successfully processed
    # else False
    # Kick -> Boolean
    def player_kick_update(self, kick):
        pass

    # Gets a placement action from the player
    # Void -> Placement
    def get_placement(self):
        pass

    # Gets a movement action from the player
    # Void -> Move
    def get_move(self):
        pass

    # Updates the player on the start of a tournament
    # returns True if the update was successfully processed
    # else False
    # Any -> Boolean
    def tournamnent_start_update(self):
        pass

    # Updates the player whether they have won the tournament
    # returns True if the update was successfully processed
    # else False
    # Boolean -> Boolean
    def tournamnent_result_update(self, won):
        pass

    
