import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../../.."))

from Fish.Player.player import Player
from Fish.Player.strategy import Strategy
from Fish.Remote.client import Client
from Fish.Remote.server import Server
from Fish.Remote.messages import Messages
from Fish.Common.state import GameState

from concurrent.futures import ThreadPoolExecutor
import socket
import unittest
import json

class TestStart(unittest.TestCase):

    def test_proper_start(self):
        mock_socket = MockServer()
        player = Player(Strategy, 0)
        client = Client("test", player, mock_socket=mock_socket)

        self.assertEqual(client.start(True), Messages.ACK)

    def test_improper_start(self):
        mock_socket = MockServer()
        player = Player(Strategy, 0)
        client = Client("test", player, mock_socket=mock_socket)

        self.assertEqual(client.start(False), Messages.ACK)
        

class TestEnd(unittest.TestCase):

    def test_won(self):
        mock_socket = MockServer()
        player = Player(Strategy, 0)
        client = Client("test", player, mock_socket=mock_socket)

        self.assertEqual(client.end(True), Messages.ACK)

    def test_lost(self):
        mock_socket = MockServer()
        player = Player(Strategy, 0)
        client = Client("test", player, mock_socket=mock_socket)

        self.assertEqual(client.end(False), Messages.ACK)


class TestPlayingAs(unittest.TestCase):

    def test_proper_color_assignment(self):
        mock_socket = MockServer()
        player = Player(Strategy, 0)
        client = Client("test", player, mock_socket=mock_socket)

        self.assertEqual(client.playing_as("red"), Messages.ACK)


class TestPlayingWith(unittest.TestCase):

    def test_proper_playing_colors(self):
        mock_socket = MockServer()
        player = Player(Strategy, 0)
        client = Client("test", player, mock_socket=mock_socket)

        self.assertEqual(client.playing_with(["red", "white"]), Messages.ACK)


class TestIniternalizeState(unittest.TestCase):

    def test_internalize_state1(self):
        mock_socket = MockServer()
        player = Player(Strategy, 0)
        client = Client("test", player, mock_socket=mock_socket)

        self.assertEqual(client.playing_with(["red", "brown", "white"]), Messages.ACK)

        player1 = {
            "color": "red",
            "score": 0,
            "places": [(0,0), (1,0), (2,0)]
        }

        player2 = {
            "color": "brown",
            "score": 0,
            "places": [(0,1), (1,1), (2,1)]
        }

        player3 = {
            "color": "white",
            "score": 0,
            "places": [(0,2), (1,2), (2,2)]
        }

        state = {
            "players": [player2, player1, player3],
            "board": [[1, 2, 0], [0, 2, 5], [0, 0, 4]]
        }

        expected = (
            [[1, 2, 0], [0, 2, 5], [0, 0, 4]],
            ['red', 'brown', 'white'],
            {
                'brown': [(0, 1), (1, 1), (2, 1)],
                'red': [(0, 0), (1, 0), (2, 0)],
                'white': [(0, 2), (1, 2), (2, 2)]
            },
            1,
            {'brown': 0, 'red': 0, 'white': 0}
        )

        self.assertEqual(client.internalize_state(state), expected)


    def test_internalize_state2(self):
        mock_socket = MockServer()
        player = Player(Strategy, 0)
        client = Client("test", player, mock_socket=mock_socket)

        self.assertEqual(client.playing_with(["red", "brown"]), Messages.ACK)

        player1 = {
            "color": "red",
            "score": 0,
            "places": [(0,0), (1,0), (2,0), (3,0)]
        }

        player2 = {
            "color": "brown",
            "score": 0,
            "places": [(0,1), (1,1), (2,1), (3,1)]
        }

        state = {
            "players": [player2, player1],
            "board": [[1, 2, 0], [0, 2, 5], [0, 0, 4], [1, 1, 4]]
        }

        expected = (
            [[1, 2, 0], [0, 2, 5], [0, 0, 4], [1, 1, 4]],
            ['red', 'brown'],
            {
                'brown': [(0, 1), (1, 1), (2, 1), (3, 1)],
                'red': [(0, 0), (1, 0), (2, 0), (3, 0)]
            },
            1,
            {'brown': 0, 'red': 0}
        )

        self.assertEqual(client.internalize_state(state), expected)


class TestSetup(unittest.TestCase):

    def test_proper_setup(self):
        mock_socket = MockServer()
        player = Player(Strategy, 0)
        client = Client("test", player, mock_socket=mock_socket)

        self.assertEqual(client.playing_with(["red", "brown"]), Messages.ACK)

        player1 = {
            "color": "red",
            "score": 0,
            "places": [(0,0)]
        }

        player2 = {
            "color": "brown",
            "score": 0,
            "places": []
        }

        state = {
            "players": [player2, player1],
            "board": [[1, 2, 0], [0, 2, 5], [0, 0, 4]]
        }

        self.assertEqual(client.setup(state), (0,1))


class TestTakeTurn(unittest.TestCase):

    def test_proper_take_turn(self):
        mock_socket = MockServer()
        player = Player(Strategy, 0)
        client = Client("test", player, mock_socket=mock_socket)


        self.assertEqual(client.playing_with(["red", "brown"]), Messages.ACK)

        player1 = {
            "color": "red",
            "score": 0,
            "places": [(0,0), (1,0), (2,0), (3,0)]
        }

        player2 = {
            "color": "brown",
            "score": 0,
            "places": [(0,1), (1,1), (2,1), (3,1)]
        }

        state = {
            "players": [player2, player1],
            "board": [[1, 2, 0], [0, 2, 5], [0, 0, 4], [1, 1, 4]]
        }

        self.assertEqual(client.take_turn(state, []), ((1, 1), (2, 2)))

class TestTournamentSignup(unittest.TestCase):

    def test_sign_up(self):
        mock_socket = MockServer()

        name = "test"
        player = Player(Strategy, 0)
        client = Client(name, player, mock_socket=mock_socket)


        self.assertTrue(client.tournament_signup())
        self.assertEqual(json.dumps(name).encode(), mock_socket.sent_message)

# TODO: If we have time test the other replies beyond just start
class TestReplyToServer(unittest.TestCase):
    def test_reply_start(self):
        mock_socket = MockServer()

        name = "test"
        player = Player(Strategy, 0)
        client = Client(name, player, mock_socket=mock_socket)

        resp_msg = json.dumps([Messages.START, [True]])
        client.reply(resp_msg)

        self.assertEqual(json.dumps('void').encode(), mock_socket.sent_message)


    def test_reply_end(self):
        mock_socket = MockServer()

        name = "test"
        player = Player(Strategy, 0)
        client = Client(name, player, mock_socket=mock_socket)

        resp_msg = json.dumps([Messages.END, [True]])
        client.reply(resp_msg)

        self.assertEqual(json.dumps('void').encode(), mock_socket.sent_message)

        resp_msg = json.dumps([Messages.END, [False]])
        client.reply(resp_msg)

        self.assertEqual(json.dumps('void').encode(), mock_socket.sent_message)


    def test_reply_playing_as(self):
        mock_socket = MockServer()

        name = "test"
        player = Player(Strategy, 0)
        client = Client(name, player, mock_socket=mock_socket)

        resp_msg = json.dumps([Messages.PLAYING_AS, ["red"]])
        client.reply(resp_msg)

        self.assertEqual(json.dumps('void').encode(), mock_socket.sent_message)


    def test_reply_playing_with(self):
        mock_socket = MockServer()

        name = "test"
        player = Player(Strategy, 0)
        client = Client(name, player, mock_socket=mock_socket)

        resp_msg = json.dumps([Messages.PLAYING_AS, [["red", "brown", "white"]]])
        client.reply(resp_msg)

        self.assertEqual(json.dumps('void').encode(), mock_socket.sent_message)

    
    def test_reply_setup(self):
        mock_socket = MockServer()

        name = "test"
        player = Player(Strategy, 0)
        client = Client(name, player, mock_socket=mock_socket)

        self.assertEqual(client.playing_with(["red", "brown"]), Messages.ACK)

        player1 = {
            "color": "red",
            "score": 0,
            "places": [(0,0), (1,0), (2,0), (3,0)]
        }

        player2 = {
            "color": "brown",
            "score": 0,
            "places": [(0,1), (1,1), (2,1)]
        }

        state = {
            "players": [player2, player1],
            "board": [[1, 2, 0], [0, 2, 5], [0, 0, 4], [1, 1, 4]]
        }

        resp_msg = json.dumps([Messages.SETUP, [state]])
        client.reply(resp_msg)

        self.assertEqual(json.dumps([1, 2]).encode(), mock_socket.sent_message)


    def test_reply_taketurn(self):
        mock_socket = MockServer()

        name = "test"
        player = Player(Strategy, 0)
        client = Client(name, player, mock_socket=mock_socket)

        self.assertEqual(client.playing_with(["red", "brown"]), Messages.ACK)

        player1 = {
            "color": "red",
            "score": 0,
            "places": [(0,0), (1,0), (2,0), (3,0)]
        }

        player2 = {
            "color": "brown",
            "score": 0,
            "places": [(0,1), (1,1), (2,1), (3,1)]
        }

        state = {
            "players": [player2, player1],
            "board": [[1, 2, 0], [0, 2, 5], [0, 0, 4], [1, 1, 4]]
        }

        resp_msg = json.dumps([Messages.TAKE_TURN, [state, []]])
        client.reply(resp_msg)

        self.assertEqual(json.dumps([[1, 1], [2, 2]]).encode(), mock_socket.sent_message)


class MockServer():
    def __init__(self, resp_message=None):
        self.resp_message = resp_message
        self.sent_message = None

    def sendall(self, message):
        self.sent_message = message

    def recv(self, buff_size):
        return self.resp_message


if __name__ == '__main__':
    unittest.main()
