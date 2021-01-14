from enum import Enum

class MsgType(Enum):
    T_START = "t-start"
    T_PROGRESS = "t-progress"
    T_END = "t-end" 
    PLAYING_AS = "playing-as"
    T_ACTION = "t-action"
    G_START = "g-start"
    G_ACTION = "g-action"
    G_KICK = "g-kick"


class Message:
    pass