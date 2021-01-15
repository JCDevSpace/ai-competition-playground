from Game.Common.single_agent_state import SingleAgentState
from Game.Common.multi_agent_state import MultiAgentState
from Game.Common.checker_board import CheckerBoard
from Game.Common.marble_board import MarbleBoard
from Game.Common.fish_board import FishBoard


class GameBuilder:

    def __init__(self, players, game_config):
        self.players = players
        self.game_config = game_config

    def build_board(self):
        if self.game_config["board_type"] == "checker":
            return CheckerBoard()
        else:
            board = FishBoard(self.players, 4,4)
            if board.make_random_board():
                return board

    def build_state(self):
        return MultiAgentState(self.players, self.build_board())

    def state_from_config(self):
        pass

    def board_from_config(self):
        pass

    @classmethod
    def state_from_info(cls, state_info):
        try:
            board = cls.board_from_info(state_info["board"])
            if state_info["multi-agent"]:
                state = MultiAgentState(state_info["players"], board)
        except Exception as e:
            print(e)
        return False

    @classmethod
    def board_from_info(cls, board_info):
        pass