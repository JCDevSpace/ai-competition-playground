from Game.Common.single_agent_state import SingleAgentState
from Game.Common.multi_agent_state import MultiAgentState
from Game.Common.i_state import StateType

from Game.Common.checker_board import CheckerBoard
from Game.Common.marble_board import MarbleBoard
from Game.Common.fish_board import FishBoard
from Game.Common.i_board import BoardType

from enum import Enum

import traceback


"""
The game builder module encapsulates the various functions for building the game elements either from configurations or information that got sent over the network as specificed in the message protocol.
"""


class BuildType(Enum):
    """
    A BuildType is an enum that represents the type of game element to construct.
    """
    STATE_CONFIG = "state-config"
    BOARD_CONFIG = "board-config"
    STATE_INFO = "state-info"
    BOARD_INFO = "board-info"
    INVALID = "invalid"

    def is_valid(self):
        return self != self.INVALID


def config2multistate(players, config):
    """Builds a MultiAgentState with the given players and configurations.

    Args:
        players (list): a list of player colors
        config (dict): a dictionary of conifgurations

    Returns:
        MultiAgentState: a multi agent game state
    """
    board = board_from_config(players, config)
    if board:
        return MultiAgentState(players, board)
    return False

def config2singlestate(player, config):
    """Builds a SingleAgentState with the given player and configurations.

    Args:
        players (tr): a string of player color
        config (dict): a dictionary of conifgurations

    Returns:
        SingleAgentState: a single agent game state
    """
    board = board_from_config(player, config)
    if board:
        return SingleAgentState(player, board)
    return False

def config2marbleboard(player, config):
    """Builds a MarbleBoard with the given player and configurations.

    Args:
        players (str): a string of player color
        config (dict): a dictionary of conifgurations

    Returns:
        MarbleBoard: a marble board
    """
    return MarbleBoard()

def config2checkerboard(players, config):
    """Builds a Checker with the given players and configurations.

    Args:
        players (list): a list of player colors
        config (dict): a dictionary of conifgurations

    Returns:
        CheckerBoard: a checker board
    """
    return CheckerBoard()

def config2fishboard(players, config):
    """Builds a FishBoard with the given players and configurations.

    Args:
        players (list): a list of player colors
        config (dict): a dictionary of conifgurations

    Returns:
        FishBoard: a fish board
    """
    board = FishBoard(players, 4, 4)
    if board.make_random_board():
        return board
    return False

def info2multistate(cls, info):
    """Builds a MultiAgentState with the given info as specified in the message protocol.

    Args:
        info (dict): a dictionary of info

    Returns:
        MultiAgentState: a multi agent game state
    """
    board = cls.board_from_info(info["board"])
    if board:
        state = SingleAgentState(info["players"], board)
        for player, score in info["scores"]:
            if not state.set_scores(player, score):
                return False
        return state
    return False

def info2singlestate(cls, info):
    """Builds a SingleAgentState with the given info as specified in the message protocol.

    Args:
        info (dict): a dictionary of info

    Returns:
        SingleAgentState: a single agent game state
    """
    board = cls.board_from_info(info["board"])
    if board:
        state = SingleAgentState(info["players"][0], board)
        for player, score in info["scores"]:
            if not state.set_scores(player, score):
                return False
        return state
    return False

def info2marbleboard(info):
    """Builds a MarbleBoard with the given info as specified in the message protocol.

    Args:
        info (dict): a dictionary of info

    Returns:
        MarbleBoard: a marble board
    """
    board = MarbleBoard()
    if board.set_layout(info["layout"]):
        return board
    return False

def info2checkerboard(info):
    """Builds a CheckerBoard with the given info as specified in the message protocol.

    Args:
        info (dict): a dictionary of info

    Returns:
        CheckerBoard: a checker board
    """
    board = CheckerBoard()
    if board.set_layout(info["layout"]) \
            and board.set_avatars(info["avatars"]):
        return board
    return False

def info2fishboard(info):
    """Builds a FishBoard with the given info as specified in the message protocol.

    Args:
        info (dict): a dictionary of info

    Returns:
        FishBoard: a fish board
    """
    board = FishBoard(info["players"], 4, 4)
    if board.set_layout(info["layout"]) \
            and board.set_avatars(info["avatars"]):
        return board
    return False


def state_from_config(players, game_config):
    """Builds a state from the given players and game conifguration.

    Args:
        players (list): a list of player colors
        game_config (dict): a dictionary of game configurations

    Returns:
        IState: a game state object
    """
    try:
        state_type = StateType.value2type(game_config["state_type"])
        state = build(BuildType.STATE_CONFIG, state_type, [players, game_config["board"]])
        if state:
            return state
    except Exception:
        print(traceback.format_exc())
    return False

def board_from_config(players, game_config):
    """Builds a board form the given players and game configuration.

    Args:
        players (list): a list of player colors
        game_config (dict): a dictionary of game configurations

    Returns:
        IBoard: a game board object
    """
    try:
        print("Builder got config", game_config)
        board_type = BoardType.value2type(game_config["board_type"])
        board = build(BuildType.BOARD_CONFIG, board_type, [players, game_config["config"]])
        if board:
            return board
    except Exception :
        print(traceback.format_exc())
    return False

def state_from_info(state_info):
    """Builds a state from the given state_info as specified in the message protocol.

    Args:
        game_config (dict): a dictionary of info

    Returns:
        IState: a game state object
    """
    try:
        state_type = StateType.value2type(state_info["state-type"])
        state = build(BuildType.STATE_INFO, state_type, [state_info["info"]])
        if state:
            return state
    except Exception:
        print(traceback.format_exc())
    return False

def board_from_info(board_info):
    """Builds a board form the given board_info as specified in the message protocol.

    Args:
        game_config (dict): a dictionary of info

    Returns:
        IBoard: a game board object
    """
    try:
        board_type = BoardType.value2type(board_info["board-type"])
        board = build(BuildType.BOARD_INFO, board_type, [board_info["info"]])
        if board:
            return board
    except Exception:
        print(traceback.format_exc())
    return False

def build(build_type, result_type, build_mat):
    """Builds a game component of the resulting type with the given build method type and building materials(info or configurations).

    Args:
        build_type (BuildType): a member of the BuildType enum
        result_type union(StateType, BoardType): a memebr of the StateType enum or BoardType enum
        build_mat (list): a list of building materials including player list, info dictionary or configuration dictionary

    Returns:
        x: the yeild of the builder for the given build method type
    """
    if result_type.is_valid():
        builder_table = BUILDER_TABLES[build_type]
        builder = builder_table[result_type]
        result = builder(*build_mat)
        if result:
            return result
    return False

CONFIG_STATE_BUILDERS = {
    StateType.MULTIAGENT: config2multistate,
    StateType.SINGLEAGENT: config2singlestate
}

CONFIG_BOARD_BUILDERS = {
    BoardType.MARBLE: config2marbleboard,
    BoardType.CHECKER: config2checkerboard,
    BoardType.FISH: config2fishboard
}

INFO_STATE_BUILDERS = {
    StateType.MULTIAGENT: info2multistate,
    StateType.SINGLEAGENT: info2singlestate
}

INFO_BOARD_BUILDERS = {
    BoardType.MARBLE: info2marbleboard,
    BoardType.CHECKER: info2checkerboard,
    BoardType.FISH: info2fishboard
}

BUILDER_TABLES = {
    BuildType.STATE_CONFIG: CONFIG_STATE_BUILDERS,
    BuildType.BOARD_CONFIG: CONFIG_BOARD_BUILDERS,
    BuildType.STATE_INFO: INFO_STATE_BUILDERS,
    BuildType.BOARD_INFO: INFO_BOARD_BUILDERS
}
