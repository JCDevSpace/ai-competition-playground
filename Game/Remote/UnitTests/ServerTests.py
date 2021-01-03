import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../../.."))

from Fish.Remote.server import Server
from Fish.Remote.remote_player import RemotePlayer
from Fish.Player.player import Player
from Fish.Player.strategy import Strategy

import unittest
import json
import time 

class TestSignup(unittest.TestCase):
    def test_maximum_signup(self):
        mock_socket = MockSocket()
        server = Server(mock_socket=mock_socket)

        successfully_signed_up_players = server.signup_phase()
        self.assertTrue(successfully_signed_up_players)
        self.assertEqual(server.MAX_SIGNUP, len(server.connections))

    def test_minimum_signup(self):
        mock_socket = MockSocket(Server.MIN_SIGNUP)
        server = Server(mock_socket=mock_socket)

        successfully_signed_up_players = server.signup_phase()
        self.assertTrue(successfully_signed_up_players)
        self.assertEqual(Server.MIN_SIGNUP, len(server.connections))

class TestAccept(unittest.TestCase):
    def test_accept_min_and_more_signup_time(self):
        mock_socket = MockSocket(Server.MIN_SIGNUP)
        server = Server(mock_socket=mock_socket)

        server.connections = [i for i in range(Server.MIN_SIGNUP)]
        server.signup_start_time = time.time()

        self.assertTrue(server.accept_signup())

    def test_accept_min_and_no_signup_time(self):
        mock_socket = MockSocket(Server.MIN_SIGNUP)
        server = Server(mock_socket=mock_socket)

        server.connections = [i for i in range(Server.MIN_SIGNUP)]
        server.signup_start_time = time.time() - Server.SIGNUP_LENGTH

        self.assertFalse(server.accept_signup())

    def test_accept_max(self):
        mock_socket = MockSocket(Server.MIN_SIGNUP)
        server = Server(mock_socket=mock_socket)

        server.connections = [i for i in range(Server.MAX_SIGNUP)]
        server.signup_start_time = time.time()

        self.assertFalse(server.accept_signup())

    def test_accept_too_many(self):
        mock_socket = MockSocket(Server.MIN_SIGNUP)
        server = Server(mock_socket=mock_socket)

        server.connections = [i for i in range(Server.MAX_SIGNUP + 1)]
        server.signup_start_time = time.time()

        self.assertRaisesRegex(ValueError, "More than the maximum allowable players have signed up",
        server.accept_signup)

class TestStartTournament(unittest.TestCase):
    def test_start_tournament(self):
        mock_socket = MockSocket()
        server = Server(mock_socket=mock_socket)
        server.make_players_from_connections = lambda: [Player(Strategy, i, depth=1) for i in range(10)]

        winner_count, kicked_count = server.start_tournament()
        self.assertEqual(1, winner_count)
        self.assertEqual(0, kicked_count)

class TestRunTournament(unittest.TestCase):
    def test_run_tournament(self):
        mock_socket = MockSocket()
        server = Server(mock_socket=mock_socket)
        server.make_players_from_connections = lambda: [Player(Strategy, i, depth=1) for i in range(10)]

        winner_count, kicked_count = server.run()
        self.assertEqual(1, winner_count)
        self.assertEqual(0, kicked_count)

class TestMakePlayersFromConnections(unittest.TestCase):
    def test_make_players_from_connections(self):
        mock_socket = MockSocket()
        server = Server(mock_socket=mock_socket)
        connections = {}
        for i in range(10):
            connections['player' + str(i)] = MockSocket()
        
        server.connections = connections
        players = server.make_players_from_connections()

        self.assertEqual(10, len(players))
        for player in players:
            self.assertTrue(isinstance(player, RemotePlayer))

class MockSocket:
    def __init__(self, player_count=999):
       self.name = "Player"
       self.i = 0
       self.message = None
       self.player_count = player_count

    def sendall(self, message):
        self.message = message

    def settimeout(self, timeout):
        pass

    def listen(self):
        pass

    def accept(self):
        self.i += 1
        if self.i > self.player_count:
            time.sleep(Server.SIGNUP_LENGTH)
            return (MockConnection(''), None)
        return (MockConnection(self.name + str(self.i)), None)
class MockConnection:
    def __init__(self, name=None):
        self.name = name

    def recv(self, buff_size):
        return json.dumps(self.name)


if __name__ == '__main__':
    unittest.main()
