
# A Message is a {'type': String, 'content': Object}
# The referee communicates to the players and observers by sending them Messages
# The type field tells the player what it needs to do with the content.
# There are 5 types of messages
# - color_assignment
# - initial_state
# - placement
# - movement
# - player_kick
#
# The content of the message tells the player the information
# it needs to perform the changes according to the messgae
class Message():
    COLOR_ASSIGNMENT = 'color_assignment'
    INITIAL_STATE = 'initial_state'
    PLACEMENT = 'placement'
    MOVEMENT = 'movement'
    PLAYER_KICK = 'player_kick'
    TOURNAMENT_START = 'tournament_start'
    TOURNAMENT_RESULT = 'tournamnent_result'

    def generate_color_assignment(color):
        return {'type': Message.COLOR_ASSIGNMENT, 'content': color }

    def generate_initial_state(state):
        return {'type': Message.INITIAL_STATE, 'content': state}

    def generate_placement(placement):
        return {'type': Message.PLACEMENT, 'content': placement}

    def generate_movement(move):
        return {'type': Message.MOVEMENT, 'content': move}

    def generate_kick(color):
        return {'type': Message.PLAYER_KICK, 'content': color}

    def generate_notify_start():
        return {'type': Message.TOURNAMENT_START, 'content': None}

    def generate_notify_results(won):
        return {'type': Message.TOURNAMENT_RESULT, 'content': won}
