import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()

import json

# A Formatted representation is when the internal representation
# is converted into the format of the JSON messages, but it is
# not JSON yet, because the message is not converted into JSON
# until the whole message has been formatted

# A Formatted-Player is of the form:
# { "color" : Color,
#   "score" : Natural,
#   "places" : [Position, ..., Position]
# }

# A Formatted-State is of the form:
# {
#   players: [Formatted-Player, ..., Formatted-Player],
#   board: Board,
# }

# A Formatted-Move is of the form:
# [(Natural, Natural), (Natural, Natural)]

# An Argument is one of:
# - Boolean
# - Color
# - [Color, ..., Color]
# - Formatted-State
# - Formatted-State, [Formatted-Move, Formatted-Move, Formatted-Move]

# This class stores all the constants used in Messages between proxies,
# and contains methods for converting internal representations to Formatted
# representations
class Messages:
    # Server-To-Client-Name
    START = "start"
    END = "end"
    PLAYING_AS = "playing-as"
    PLAYING_WITH = "playing-with"
    SETUP = "setup"
    TAKE_TURN = "take-turn"

    # Client-To-Server-Name
    VOID = "void"
    POSITION = "position"
    ACTION = "action"
    INVALID = "invalid"


    # Converts internally represented players into the Formatted form
    # List[Color], List[Penguin], List[Score], Natural -> Formatted-State
    def convert_players(colors, penguins, scores, turn):
        players = []
        for i in range(len(colors)):
            current_color = colors[(i + turn) % len(colors)]
            players.append({
                "color": current_color,
                "score": scores[current_color],
                "places": penguins[current_color],
            })
        return players


    # Converts an internally represented state into the Formatted form
    # State -> Formatted-State
    def convert_state(state):
        board, players, penguins, turn, scores = state

        return {
            "players": Messages.convert_players(colors, penguins, scores, turn),
            "board": board
        }


    # Converts internally represented actions into the Formatted form
    # List[Move] -> List[Formatted-Move]
    def convert_actions(actions):
        convertedActions = []
        for _, start, end in actions:
            if not start:
                convertedActions.append(False)
            else:
                convertedActions.append([start, end])
        return convertedActions


    # Takes a name of the function and the Formatted arguments to call it with,
    # and makes it into JSON
    # Server-To-Client-Name, List[Argument] -> JSON
    def encode(type, args):
        return json.dumps([name, [*args])])


    def decode(message):
        pass
    
    # Checks if a provided parameter is a valid position 
    # Any -> Boolean
    def valid_position(position):
        return (isinstance(position, list) and
            len(position) == 2 and
            isinstance(position[0], int) and 
            isinstance(position[1], int) and 
            position[0] >= 0 and
            position[1] >= 0)
    
    # Checks if a provided parameter is a valid action 
    # Any -> Boolean
    def valid_action(action):
        return (isinstance(action, list) and
            len(action) == 2 and
            Messages.valid_position(action[0]) and
            Messages.valid_position(action[1]))

    # Converts the response message bytes into internal python representations
    # else if the response message is an invalid json return False
    def convert_message(message):
        try:
            response = json.loads(message)
            return response
        except:
            return False

    
    def response_type(response):
        if response == Messages.VOID:
            return Messages.VOID
        else if Messages.valid_position(response):
            return Messages.POSITION
        else if Messages.valid_action(response):
            return Messages.ACTION
        else:
            return Messages.INVALID

            
