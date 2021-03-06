from src.common.single_agent_state import SingleAgentState
from src.common.multi_agent_state import MultiAgentState
from src.common.i_state import StateType

from src.common.checker_board import CheckerBoard
from src.common.marble_board import MarbleBoard
from src.common.fish_board import FishBoard
from src.common.i_board import BoardType

from enum import Enum


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


def config2multistate(players, game_config):
    """Builds a MultiAgentState with the given players and configurations.

    Args:
        players (list): a list of player colors
        game_config (dict): a dictionary of conifgurations

    Returns:
        MultiAgentState: a multi agent game state
    """
    board = board_from_config(players, game_config["board"])
    if board:
        return MultiAgentState(players, board)
    return False

def config2singlestate(players, game_config):
    """Builds a SingleAgentState with the given player and configurations.

    Args:
        players (list): a list of player color
        game_config (dict): a dictionary of conifgurations

    Returns:
        SingleAgentState: a single agent game state
    """
    board = board_from_config(players, game_config["board"])
    if board:
        return SingleAgentState(players[0], board)
    return False

def config2marbleboard(players, board_config):
    """Builds a MarbleBoard with the given player and configurations.

    Args:
        players (list): a list of player color
        board_config (dict): a dictionary of conifgurations

    Returns:
        MarbleBoard: a marble board
    """
    return MarbleBoard()

def config2checkerboard(players, board_config):
    """Builds a Checker with the given players and configurations.

    Args:
        players (list): a list of player colors
        board_config (dict): a dictionary of conifgurations

    Returns:
        CheckerBoard: a checker board
    """
    return CheckerBoard()

def config2fishboard(players, board_config):
    """Builds a FishBoard with the given players and configurations.

    Args:
        players (list): a list of player colors
        board_config (dict): a dictionary of conifgurations

    Returns:
        FishBoard: a fish board
    """
    board = FishBoard(players, 6, 6)
    if board.make_random_board():
        return board
    return False

def info2multistate(info):
    """Builds a MultiAgentState with the given info as specified in the message protocol.

    Args:
        info (dict): a dictionary of info

    Returns:
        MultiAgentState: a multi agent game state
    """
    board = board_from_info(info["players"], info["board"])
    if board:
        state = MultiAgentState(info["players"], board)
        for player, score in info["scores"].items():
            if not state.set_score(player, score):
                return False
        return state
    return False

def info2singlestate(info):
    """Builds a SingleAgentState with the given info as specified in the message protocol.

    Args:
        info (dict): a dictionary of info

    Returns:
        SingleAgentState: a single agent game state
    """
    board = board_from_info(info["players"], info["board"])
    if board:
        state = SingleAgentState(info["players"][0], board)
        for player, score in info["scores"].items():
            if not state.set_score(player, score):
                return False
        return state
    return False

def info2marbleboard(players, board_info):
    """Builds a MarbleBoard with the given info as specified in the message protocol.

    Args:
        info (dict): a dictionary of info

    Returns:
        MarbleBoard: a marble board
    """
    board = MarbleBoard()
    if board.set_layout(board_info["layout"]):
        return board
    return False

def info2checkerboard(players, board_info):
    """Builds a CheckerBoard with the given info as specified in the message protocol.

    Args:
        info (dict): a dictionary of info

    Returns:
        CheckerBoard: a checker board
    """
    board = CheckerBoard()
    if board.set_layout(board_info["layout"]):
        avatars = info2avatars(board_info["avatars"])
        if board.set_avatars(avatars):
            return board
    return False

def info2fishboard(players, board_info):
    """Builds a FishBoard with the given info as specified in the message protocol.

    Args:
        info (dict): a dictionary of info

    Returns:
        FishBoard: a fish board
    """
    board = FishBoard(players, 4, 4)
    if board.set_layout(board_info["layout"]):
        avatars = info2avatars(board_info["avatars"])
        if board.set_avatars(avatars):
            return board
    return False

def info2avatars(avatar_info):
    """Convertes the json object of lists of avatar positions to internal Posn lists

    Args:
        avatar_info (dict): dictionary containing with player color as key and the corresponding 2D json array as the list it's avatar positions
    """
    return {color:[tuple(posn) for posn in posns] for color, posns in avatar_info.items()}

def state_from_config(players, game_config):
    """Builds a state from the given players and game conifguration.

    Args:
        players (list): a list of player colors
        game_config (dict): a dictionary of game configurations

    Returns:
        IState: a game state object
    """
    state = build(["state_type", "config"], game_config, [players], CONFIG_STATE_BUILDERS, StateType)
    if state:
        return state
    return False

def board_from_config(players, board_config):
    """Builds a board form the given players and board configuration.

    Args:
        players (list): a list of player colors
        board_config (dict): a dictionary of game configurations

    Returns:
        IBoard: a game board object
    """
    board = build(["board_type", "config"], board_config, [players], CONFIG_BOARD_BUILDERS, BoardType)
    if board:
        return board
    return False

def state_from_info(state_info):
    """Builds a state from the given state_info as specified in the message protocol.

    Args:
        game_config (dict): a dictionary of info

    Returns:
        IState: a game state object
    """
    state = build(["state-type", "info"], state_info, [], INFO_STATE_BUILDERS, StateType)
    if state:
        return state
    return False

def board_from_info(players, board_info):
    """Builds a board form the given board_info as specified in the message protocol.

    Args:
        game_config (dict): a dictionary of info

    Returns:
        IBoard: a game board object
    """
    board = build(["board-type", "info"], board_info, [players], INFO_BOARD_BUILDERS, BoardType)
    if board:
        return board
    return False

def build(mat_keys, mat_box, mats, builder_table, result_enum):
    """Builds the concrete game component object.

    Args:
        mat_keys (list): a list of string keys
        mat_box (dict): a dictionary to get information using the keys from
        mats (list): a list of existing information without need for extraction
        builder_table (dict): a ditionary of builders to handle the actual building of the game component
        result_enum union(StateType, BoardType): a StateType enum of BoardType enum indicating the catergory of result concrete component to build

    Returns:
        union(IState, IBoard, False): a builde state or board, otherwise False for failing to build the game component
    """
    extracted = extract_mats(result_enum, mat_keys, mat_box)
    if extracted and extracted[0].is_valid():
            mats.append(extracted[1])
            builder = builder_table[extracted[0]]
            result = builder(*mats)
            if result:
                return result
    return False

def extract_mats(result_enum, mat_keys, mat_box):
    """Extracts the build result type and the dictionary of information.

    Args:
        result_enum union(StateType, BoardType): a member from the StateType enum or from the BoardType enum
        mat_keys (str): dictionary keys to lookup stuff fro mthe dict
        mat_box (dict): a dictionary of game information or configuration

    Returns:
        union(tuple, False): a tuple with the first the build result type and second the information for building or False for failing to extract the proper information from the dictionary
    """
    try:
        result_type = result_enum.value2type(mat_box[mat_keys[0]])
        mats = mat_box[mat_keys[1]]
        return result_type, mats
    except Exception:
        pass
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