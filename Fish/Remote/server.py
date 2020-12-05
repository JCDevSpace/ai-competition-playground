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

from Fish.Admin.game_visualizer import GameVisualizer

BUFF_SIZE = 1024 #bytes
INTERACTION_TIMEOUT = 16 #seconds
SIGNUP_LENGTH = 3 #seconds
MAX_NAME_LENGTH = 12
MAX_SIGNUP = 10
MIN_SIGNUP = 5

DEFAULT_ROWS = 5
DEFAULT_COLS = 5
DEFAULT_FISH = 2

class Server:

    def __init__(self, hostname="localhost", port=13452, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, fish=DEFAULT_FISH):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((hostname, port))

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

    def signup_phase(self):
        self.sock.listen()
        self.sock.settimeout(INTERACTION_TIMEOUT)
        self.signup_start_time = time.time()
        repeated = False
        while self.accept_signup():
            try:
                connection, _ = self.sock.accept()
                recv_data = connection.recv(BUFF_SIZE)
                name = json.loads(recv_data)
                if len(name) <= MAX_NAME_LENGTH:
                    self.connections[name] = connection
                now = time.time()
                if not repeated and (now - self.signup_start_time) > SIGNUP_LENGTH:
                    self.signup_start_time = now
                    repeated = True
            except Exception as e:
                pass

        return len(self.connections) >= MIN_SIGNUP

    def accept_signup(self):
        if len(self.connections) == MAX_SIGNUP:
            return False

        now = time.time()
        if (now - self.signup_start_time) > SIGNUP_LENGTH:
            if len(self.connections) >= MIN_SIGNUP:
                return False

        return True

    def start_tournament(self):
        print('started tournament!')
        remote_players = []
        for signup_age, name in enumerate(self.connections):
            remote_players.append(RemotePlayer(name, signup_age, self.connections[name], INTERACTION_TIMEOUT, BUFF_SIZE))
        observer = GameVisualizer()
        tournament_manager = Manager(remote_players, self.rows, self.cols, self.fish, observer)
        return tournament_manager.run_tournament()