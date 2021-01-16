from Game.Common.single_agent_state import SingleAgentState
from Game.Common.multi_agent_state import MultiAgentState
from Game.Common.i_state import StateType

from Game.Common.checker_board import CheckerBoard
from Game.Common.marble_board import MarbleBoard
from Game.Common.fish_board import FishBoard
from Game.Common.i_board import BoardType


class GameBuilder:
    """
    GameBuilder is a static class that encapsulates the various functions for building the game elements either from configurations or information that got sent over the network as specificed in the message protocol.
    """
    
    CONFIG_STATE_BUILDERS = {
        StateType.MULTIAGENT: GameBuilder.config2multistate,
        StateType.SINGLEAGENT: GameBuilder.config2singlestate
    }
    CONFIG_BOARD_BUILDERS = {
        BoardType.MARBLE: GameBuilder.config2marbleboard,
        BoardType.CHECKER: GameBuilder.config2checkerboard,
        BoardType.FISH: GameBuilder.config2fishboard
    }

    INFO_STATE_BUILDERS = {
        StateType.MULTIAGENT: GameBuilder.info2multistate,
        StateType.SINGLEAGENT: GameBuilder.info2singlestate
    }

    INFO_BOARD_BUILDERS = {
        BoardType.MARBLE: GameBuilder.info2marbleboard,
        BoardType.CHECKER: GameBuilder.info2checkerboard,
        BoardType.FISH: GameBuilder.info2fishboard
    }

    @classmethod
    def config2multistate(cls, players, config):
        board = cls.board_from_config(players, config)
        if board:
            return MultiAgentState(players, board)
        return False

    @classmethod
    def config2singlestate(cls, players, config):
        board = cls.board_from_config(players, config)
        if board:
            return SingleAgentState(players, board)
        return False

    @staticmethod
    def config2marbleboard(players, config):
        return MarbleBoard()

    @staticmethod
    def config2checkerboard(players, config):
        return CheckerBoard()

    @staticmethod
    def config2fishboard(players, config):
        return FishBoard(players, 4, 4)

    @classmethod
    def info2multistate(cls, info):
        board = cls.board_from_info(info)
        if board:
            return MultiAgentState(info["players"], board)
        return False

    @classmethod
    def info2singlestate(cls, info):
        board = cls.board_from_info(info)
        if board:
            return SingleAgentState(info["players"], board)
        return False

    @staticmethod
    def info2marbleboard(info):
        board = MarbleBoard()
        board.set_layout(info["layout"])
        return board

    @staticmethod
    def info2checkerboard(info):
        board = CheckerBoard()
        board.set_layout(info["layout"])
        board.set_avatars(info["avatars"])
        return board

    @staticmethod
    def info2fishboard(info):
        board = FishBoard(info["players"], 4, 4)
        board.set_layout(info["layout"])
        board.set_avatars(info["avatars"])
        return board

    @classmethod
    def state_from_info(cls, players, game_config):
        try:
            state_type = StateType.value2type(game_config["state-type"])
            if state_type != StateType.INVALID:
                state_builder = cls.CONFIG_STATE_BUILDERS(state_type)
                state = state_builder(game_config["config"])
                if state:
                    return state
        except Exception as e:
            print(e)
        return False

    @classmethod
    def board_from_config(cls, players, game_config):
        try:
            board_type = BoardType.value2type(game_config["board-type"])
            if board_type != BoardType.INVALID:
                board_builder = cls.CONFIG_BOARD_BUILDERS(board_type)
                board = board_builder(game_config["config"])
                if board:
                    return board
        except Exception as e:
            print(e)
        return False

    @classmethod
    def state_from_info(cls, state_info):
        try:
            state_type = StateType.value2type(state_info["state-type"])
            if state_type != StateType.INVALID:
                state_builder = cls.INFO_STATE_BUILDERS(state_type)
                state = state_builder(state_info["info"])
                if state:
                    return state
        except Exception as e:
            print(e)
        return False

    @classmethod
    def board_from_info(cls, board_info):
        try:
            board_type = BoardType.value2type(board_info["board-type"])
            if board_type != BoardType.INVALID:
                board_builder = cls.INFO_BOARD_BUILDERS(board_type)
                board = board_builder(board_info["info"])
                if board:
                    return board
        except Exception as e:
            print(e)
        return False
