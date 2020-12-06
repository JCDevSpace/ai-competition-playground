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

class TestStart(unittest.TestCase):

    def test_proper_start(self):
        player = Player(Strategy, 0)
        client = Client("test", player)

        self.assertEqual(client.start(True), Messages.ACK)

    def test_improper_start(self):
        player = Player(Strategy, 0)
        client = Client("test", player)

        self.assertEqual(client.start(False), Messages.ACK)


class TestEnd(unittest.TestCase):

    def test_won(self):
        player = Player(Strategy, 0)
        client = Client("test", player)

        self.assertEqual(client.end(True), Messages.ACK)

    def test_lost(self):
        player = Player(Strategy, 0)
        client = Client("test", player)

        self.assertEqual(client.end(False), Messages.ACK)


class TestPlayingAs(unittest.TestCase):

    def test_proper_color_assignment(self):
        player = Player(Strategy, 0)
        client = Client("test", player)

        self.assertEqual(client.playing_as("red"), Messages.ACK)


class TestPlayingWith(unittest.TestCase):

    def test_proper_playing_colors(self):
        player = Player(Strategy, 0)
        client = Client("test", player)

        self.assertEqual(client.playing_with(["red", "white"]), Messages.ACK)


class TestIniternalizeState(unittest.TestCase):

    def test_internalize_state1(self):
        player = Player(Strategy, 0)
        client = Client("test", player)

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
        player = Player(Strategy, 0)
        client = Client("test", player)
        
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
        player = Player(Strategy, 0)
        client = Client("test", player)
        
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
        player = Player(Strategy, 0)
        client = Client("test", player)
        
        
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

class TestTournamentSingup(unittest.TestCase):

    def test_proper_sign_up(self):
        server = MockServer(12345)
        ret = server.start()

        name = "test"
        player = Player(Strategy, 0)
        client = Client(name, player, server_port=12345)

        self.assertTrue(client.tournament_signup())
        self.assertEqual(ret.result(2), name)

    def test_bad_sign_up(self):
        server = MockServer(12345)
        ret = server.start()


        player = Player(Strategy, 0)
        client = Client("test", player)

        self.assertFalse(client.tournament_signup())
        self.assertIsNone(ret.result(2))


if __name__ == '__main__':
    unittest.main()
