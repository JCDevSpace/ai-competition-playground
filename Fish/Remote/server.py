import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../.."))

import socket
import json
import time
from collections import OrderedDict

from Fish.Admin.manager import Manager
from Fish.Remote.remote_player import RemotePlayer
from Fish.Common.util import safe_execution
from Fish.Common.util import parse_json

# Server that accepts sign-ups. If a minimum number of players
# sign up it creates a tournament manager than runs a tournament.
# It closes itself when it is finished.

DEFAULT_ROWS = 5
DEFAULT_COLS = 5
DEFAULT_FISH = 2
class Server:
    BUFF_SIZE = 1024 #bytes
    INTERACTION_TIMEOUT = 16 #seconds
    SIGNUP_LENGTH = 30 #seconds
    MIN_NAME_LENGTH = 1
    MAX_NAME_LENGTH = 12
    MAX_SIGNUP = 10
    MIN_SIGNUP = 5

    # Parameters
    # hostname: String
    #     Name of the host that this server runs on
    # port: Natural
    #     Number of the port that this server runs on
    # rows: Natural
    #     Number of rows the Tournament Manager will be created with
    # cols: Natural
    #     Number of cols the Tournament Manager will be created with
    # fish: Natural
    #     Number of fish the Tournament Manager will request be on tiles
    def __init__(self, hostname="localhost", port=1234, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, fish=DEFAULT_FISH, mock_socket=None):
        if not mock_socket:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((hostname, port))
        else:
            self.sock = mock_socket

        self.rows = rows
        self.cols = cols
        self.fish = fish

        self.connections = OrderedDict()

    # Run the server through the signup phase and the tournament
    # if the signup phase was successful, returns False if the
    # tournament was not ran else the number of winners and number
    # of players who failed or cheated in the tournament.
    # Void -> Union(False, (Int, Int))
    def run(self):
        success = self.signup_phase()
        if success:
            return self.start_tournament()
        self.sock.close()
        return False

    # The server awaits TCP connections according to Remote Interactions.
    # It waits for some time for at least a minimum number
    # of remote clients to connect and be represented as remote players.
    # As long as there isn’t this minimum number of clients connected at
    # the end of a waiting period, the server re-enters the waiting state once.
    # The waiting period ends if the server has accepted a maximal number
    # of client connections. Return true if a minimum number of
    # players were signed up, else false
    # void -> Boolean
    def signup_phase(self):
        self.sock.listen()
        self.sock.settimeout(self.INTERACTION_TIMEOUT)
        self.signup_start_time = time.time()
        repeated = False
        while self.accept_signup():
            try:
                connection, _ = self.sock.accept()
                recv_data = connection.recv(self.BUFF_SIZE)
                name = json.loads(recv_data)
                if self.MIN_NAME_LENGTH <= len(name) <= self.MAX_NAME_LENGTH:
                    self.connections[name] = connection
                now = time.time()
                if not repeated and (now - self.signup_start_time) > self.SIGNUP_LENGTH:
                    self.signup_start_time = now
                    repeated = True
            except Exception as e:
                print(e)
                pass

        return len(self.connections) >= self.MIN_SIGNUP

    # Helper function that determines if we should continue
    # accepting signups. If we've reached the maximum amount
    # of signups or waited past the signup length return False,
    # otherwise True
    # Void -> Boolean
    def accept_signup(self):
        if len(self.connections) > self.MAX_SIGNUP:
            raise ValueError("More than the maximum allowable players have signed up")

        if len(self.connections) == self.MAX_SIGNUP:
            return False

        now = time.time()
        if (now - self.signup_start_time) > self.SIGNUP_LENGTH:
            if len(self.connections) >= self.MIN_SIGNUP:
                return False

        return True
    
    # Creates a remote player for each of the players that signed up.
    # void -> List[Remote-Player]
    def make_players_from_connections(self):
        remote_players = []
        for signup_age, name in enumerate(self.connections):
            remote_players.append(RemotePlayer(name, signup_age, self.connections[name], self.INTERACTION_TIMEOUT, self.BUFF_SIZE))
        return remote_players

    # Creates a tournament manager and runs it with the remote players,
    # which returns the number of winners and cheating/failing players.
    # void -> Int, Int
    def start_tournament(self):
        remote_players = self.make_players_from_connections()
        tournament_manager = Manager(remote_players, self.rows, self.cols, self.fish)
        winners, kicked = tournament_manager.run_tournament()
        return len(winners), len(kicked)
