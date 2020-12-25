import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../../.."))

import unittest
import json

from Fish.Player.strategy import Strategy
from Fish.Player.player import Player
from Fish.Common.state import GameState
from Fish.Common.board import Board
from Fish.Remote.messages import Messages

class TestConvert(unittest.TestCase):

    def test_convert_state(self):
        board = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        players = ["red", "brown", "white"]
        state = GameState(board, players)

        expected = {
            "players": [
                {
                    "color": "red",
                    "score": 0,
                    "places": []
                },
                {
                    "color": "brown",
                    "score": 0,
                    "places": []
                },
                {
                    "color": "white",
                    "score": 0,
                    "places": []
                }
            ],
            "board": [[1, 2, 0], [0, 2, 5], [0, 0, 4]]
        }
        
        self.assertEqual(Messages.convert_state(state.get_game_state()), expected)


    def test_convert_action(self):
        action1 = ("red", (1,1), (2,2))
        action2 = ("brown", (1,2), (2,1))
        action3 = ("white", (0,0), (4,2))

        self.assertEqual(Messages.convert_action(action1), ((1,1), (2,2)))
        self.assertEqual(Messages.convert_action(action2), ((1,2), (2,1)))
        self.assertEqual(Messages.convert_action(action3), ((0,0), (4,2)))


    def test_convert_actions(self):
        action1 = ("red", (1,1), (2,2))
        action2 = ("brown", (1,2), (2,1))
        action3 = ("white", (0,0), (4,2))
        actions = [action1, action2, action3]

        converted_actions = [((1,1), (2,2)), ((1,2), (2,1)), ((0,0),(4,2))]

        self.assertEqual(Messages.convert_actions(actions), converted_actions)

    
class TestEncoding(unittest.TestCase):

    def test_encoding_start(self):
        expected = json.dumps(["start", [True]]).encode()

        self.assertEqual(Messages.encode(Messages.START, [True]), expected)
    
    def test_encoding_end(self):
        expected1 = json.dumps(["end", [True]]).encode()
        expected2 = json.dumps(["end", [False]]).encode()

        self.assertEqual(Messages.encode(Messages.END, [True]), expected1)
        self.assertEqual(Messages.encode(Messages.END, [False]), expected2)


    def test_encoding_playing_as(self):
        expected1 = json.dumps(["playing-as", ["red"]]).encode()
        expected2 = json.dumps(["playing-as", ["brown"]]).encode()
        
        self.assertEqual(Messages.encode(Messages.PLAYING_AS, ["red"]), expected1)
        self.assertEqual(Messages.encode(Messages.PLAYING_AS, ["brown"]), expected2)


    def test_encoding_playing_with(self):
        expected = json.dumps(["playing-with", [["red", "brown", "white"]]]).encode()
        
        self.assertEqual(Messages.encode(Messages.PLAYING_WITH, [["red", "brown", "white"]]), expected)

    def test_encoding_setup(self):
        board = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        players = ["red", "brown", "white"]
        state = GameState(board, players)

        converted_state = Messages.convert_state(state.get_game_state())

        formatted_state = {
            "players": [
                {
                    "color": "red",
                    "score": 0,
                    "places": []
                },
                {
                    "color": "brown",
                    "score": 0,
                    "places": []
                },
                {
                    "color": "white",
                    "score": 0,
                    "places": []
                }
            ],
            "board": [[1, 2, 0], [0, 2, 5], [0, 0, 4]]
        }

        expected = json.dumps(["setup", [formatted_state]]).encode()


        self.assertEqual(Messages.encode(Messages.SETUP, [converted_state]), expected)

    def test_encoding_take_turn(self):
        board = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        players = ["red", "brown", "white"]
        state = GameState(board, players)

        action1 = ("red", (1,1), (2,2))
        action2 = ("brown", (1,2), (2,1))
        action3 = ("white", (0,0), (4,2))
        actions = [action1, action2, action3]

        converted_state = Messages.convert_state(state.get_game_state())
        converted_actions = Messages.convert_actions(actions)

        formatted_state = {
            "players": [
                {
                    "color": "red",
                    "score": 0,
                    "places": []
                },
                {
                    "color": "brown",
                    "score": 0,
                    "places": []
                },
                {
                    "color": "white",
                    "score": 0,
                    "places": []
                }
            ],
            "board": [[1, 2, 0], [0, 2, 5], [0, 0, 4]]
        }

        expected = json.dumps(["take-turn", [formatted_state, [((1,1), (2,2)), ((1,2), (2,1)), ((0,0),(4,2))]]]).encode()


        self.assertEqual(Messages.encode(Messages.TAKE_TURN, [converted_state, converted_actions]), expected)



if __name__ == '__main__':
    unittest.main()