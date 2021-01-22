from Game.Common.action import action_type, ActionType
import Game.Admin.game_builder as GameBuilder
from enum import Enum
import json
import traceback


"""
The message module encapsulates the various message processing and convertion functionalities, provides the ability to convert between the different message formats specificed in the protocol into internal data presentations.

All messages are sent as json objects with the following gernal format:

{
    "msg-type": msg_type, 
    "content": json_content
}

-msg_type:
    the string value from one of the members in the MsgType enum.

-json_content:
    a json value that takes one of the specified format below:

    -name: 
        a string of at least 1 and at most 12 alphanumeric characters that represens the name of a player that signuped to the tournament.

    -color:
        a string of one of the available colors that a player can play as.

    -action:
        one of the specified json value below:

        -skip:
            a json string with the value "skip" that represents skipping a turn

        -placement:
            a posn that represents puting an avatar as the board position
        
        -movement:
            a json array of 2 posn that represents moving an avatar from one position to another, with the first as the from positions and second to

        -posn:
            a json array of 2 non-negative integer that represents positions on the 2D board, with the first value as the row index and second the column

    -state_info:
        a json object representing the game state of a board game, takes the following specified format:

        {
            "state-type": state_type,
            "info": {
                "players": [color],
                "scores": score_dict,
                "board": board_info   
            }
        }

        -state_type:
            a string that represents the available state implementations in the the system.

        -score_dict:
            a json object with player colors as keys and a corresponding non-negative interger as the score of that player.

        -board_info:
            a json object that represents the state of a game board, takes the following specified format:

            {
                "board-type": board_type,
                "info": {
                    "layout": board_layout,
                    "avatars": avatar_dict
                }
            }

            -board_type:
                a string that represents the available board implementations in the system.

            -board_layout:
                a 2D json array that represents the board grid, with the first dimension in the board rows and second columns.

            -avatar_dict:
                a json object with player colors as the keys and a corresponding list of posn that represents the positions of avatars that the player have on the board.

                **Note: this field doesn't for game types that have only one agent

The following tables specifies the different msg_typs sent from the server with the corresponding content and the expected client response:

+============+=======================+==========+
|    type    |        content        | response |
+============+=======================+==========+
| signup     | name                  | none     |
+------------+-----------------------+----------+
| t-start    | [name...]             | none     |
+------------+-----------------------+----------+
| t-progress | [[name...],[name...]] | none     |
+------------+-----------------------+----------+
| t-end      | [name...]             | none     |
+------------+-----------------------+----------+
| playing-as | color                 | none     |
+------------+-----------------------+----------+
| t-action   | state_info            | action   |
+------------+-----------------------+----------+
| g-start    | state_info            | none     |
+------------+-----------------------+----------+
| g-action   | action                | none     |
+------------+-----------------------+----------+
| g-kick     | color                 | none     |
+------------+-----------------------+----------+
"""


class MsgType(Enum):
    """
    A MsgType is an enum that represents the type of available messages in the specified protocol, the member string values of the different message types are the identifier filed in the sent message to enable proper handling on the reciever side.
    """
    SIGNUP = "signup"
    T_START = "t-start"
    T_PROGRESS = "t-progress"
    T_END = "t-end" 
    PLAYING_AS = "playing-as"
    T_ACTION = "t-action"
    G_START = "g-start"
    G_ACTION = "g-action"
    G_KICK = "g-kick"
    INVALID = "invalid"

    @classmethod
    def value2type(cls, value):
        """Determines the MsgType of the given protocol message type.

        Args:
            value (string): a string as specified in the protocol message types

        Returns:
            Msg.Type: a member of MsgType
        """
        for member in cls.__members__.values():
            if member.value == value:
                return member
        return cls.INVALID

    def is_valid(self):
        return self != self.INVALID


def decode(message):
    """Decodes the given message, determing the message type and the corresponding internal data representation given it's content, if the message is of invalid type the returns None for content.

    Args:
        message (json): a json object taking one of the values as specified in the protocol

    Returns:
        tuple: a tuple with the first a memeber from the MsgType enum and second the converted data object from the given content of the message
    """
    content = None

    try:
        msg = json.loads(message)
        print("Loaded message type", msg["msg-type"])
        msg_type = MsgType.value2type(msg["msg-type"])

        if msg_type.is_valid():
            converter = CONVERTERS[msg_type]
            ret = converter(msg["content"])
            if ret:
                content = ret
            else:
                msg_type = MsgType.INVALID
    except Exception:
        msg_type = MsgType.INVALID
        print(traceback.format_exc())
    return msg_type, content

def str_converter(value):
    """Ensure that the given value is a string, if it is returns it else return false.

    Args:
        value (x): value to be converted

    Returns:
        union(value, False): the value itself or False
    """
    if isinstance(value, str):
        return value
    return False

def list_converter(value):
    """Ensures that the given value is a list, if it is goes through all element of the list and convert each to the name strings, returns false if the given value is not a list or any of the elements in the list is not a string name.

    Args:
        value (x): value to be converted

    Returns:
        union(list, False): a list of string names of False
    """
    if isinstance(value, list):
        converted = []
        for ele in value:
            ret = str_converter(ele)
            if not ret:
                return False
            converted.append(ret)
        return converted
    return False

def list2d_converter(value):
    """Ensures that the given value is a 2d list, if it is goes through each of the list and converts it to list of name strings, returns false if the given value is not a 2d list or either of the list in the 2d list can't be properly converted to a list of string names.

    Args:
        value (x): value to be converted

    Returns:
        union(tuple, False): a tuple of the two name list or False
    """
    if isinstance(value, list) and len(value) == 2:
        list2d = []
        for l in value:
            ret = list_converter(l)
            if not ret:
                return False
            list2d.append(ret)
        return tuple(list2d)
    return False

def action_converter(value):
    """Ensure that the given value is a valid action, if it is converts it to the corresponding internal representation of the action, returns false if the given value is an invalid action.

    Args:
        value (x): value to be converted

    Returns:
        union(Action, False): the action or False
    """
    value_type = action_type(value)

    if value_type.is_valid():
        if action_type == ActionType.MOVEMENT:
            return tuple([tuple(value[0]), tuple(value[1])])
        elif action_type == ActionType.PLACEMENT:
            return tuple(value)
        else:
            return value
    return False

def state_converter(value):
    """Ensure that the given value is a valid state_info, if it is converts it to the corresponding internal representation of the state, returns false if the given value is an invalid state_info.

    Args:
        value (x): value to to converted

    Returns:
        union(IState, False): a state or False
    """
    if isinstance(value, dict) and len(value) == 2:
        ret = GameBuilder.state_from_info(value)
        if ret:
            return ret
    return False

def construct_msg(msg_type, content):
    """Constructs a message according to the specified protocol message format with the given message type and content.

    Args:
        msg_type (MsgType): a member of MsgType enum
        content (x): one of the content formats as specified

    Returns:
        str: a json formmated string as specified in the protocol
    """
    return json.dumps(
        {
            "msg-type": msg_type.value,
            "content": content
        }
    )

CONVERTERS = {
    MsgType.SIGNUP: str_converter,
    MsgType.PLAYING_AS: str_converter,
    MsgType.G_KICK: str_converter,
    MsgType.T_START: list_converter,
    MsgType.T_END: list_converter,
    MsgType.T_PROGRESS: list2d_converter,
    MsgType.G_ACTION: action_converter,
    MsgType.G_START: state_converter,
    MsgType.T_ACTION: state_converter
}