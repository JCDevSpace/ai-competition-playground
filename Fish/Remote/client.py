import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../.."))

import socket
import json
from Fish.Remote.messages import Messages

# Proxy that receives JSON from the remote_player and converts it
# into Python before calling the methods on the client player. Then
# the response from the client is returned to the remote_player.

# A Server-Message is of the form:
# [Server-To-Client-Name, List[Argument]
class Client:
    # Initializes a client that will communicate with the given server on the given port,
    # and the given player.
    # String, Player_Interface, String, Natural, Natural -> Client
    # Parameters:
    # name: String
    #     The name of the player consisting of at least one
    #     and at most 12 alphabetical ASCII characters
    # client_player: Player
    #     Local Player
    # server_host: String
    #     The host of the remote player that this client will communicate with
    # server_port: Natural
    #     Port number of the remote player that this client will communicate with
    # buff_size: Natural
    #     Number of bytes this client is willing to receive from the remote player
    def __init__(self, name, client_player, server_host="localhost", server_port=1234, buff_size=1024, mock_socket=None):
        self.name = name
        self.client_player = client_player

        self.server_host = server_host
        self.server_port = server_port
        self.buff_size = buff_size

        self.stopped = False
        self.colors = []

        if not mock_socket:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_host, self.server_port))
        else:
            self.sock = mock_socket

    # Starts the client by signing up the player for a tournament with the server
    # then sit and waits for messages from the server and responses correspondingly
    # until the client is stopped
    # void -> void
    def run(self):
        if self.tournament_signup():
            self.process_messages()

    # Signs the client player up for a tournament with the server
    # and return True else if the connection of signup failed returns
    # void -> False
    def tournament_signup(self):
        try:
            self.sock.sendall(json.dumps(self.name).encode())
            return True
        except Exception as e:
            return False

    # Waits and recives messages from the server and executes the corresponding
    # action for the server request for the the recieved message,
    # stops receiving messages when the client is stopped.
    # void -> void
    def process_messages(self):
        while not self.stopped:
            try:
                req_msg = self.sock.recv(self.buff_size)
                if req_msg:
                    self.reply(req_msg)
            except Exception as e:
                raise e

    # Takes a request message and passes it to the
    # appropriate handler based on the Server-To-Client-Name.
    # Sends the converted player response to the remote player
    # Server-Message -> void
    def reply(self, req_msg):
        req_handler_table = {
            Messages.START: self.start,
            Messages.END: self.end,
            Messages.PLAYING_AS: self.playing_as,
            Messages.PLAYING_WITH: self.playing_with,
            Messages.SETUP: self.setup,
            Messages.TAKE_TURN: self.take_turn
        }

        converted_request = Messages.convert_message(req_msg)
        if converted_request:
            req_type = converted_request[0]
            handler = req_handler_table[req_type]
            client_response = handler(*converted_request[1])
            self.sock.sendall(json.dumps(client_response).encode())

    # Informs the player that the tournament has started
    # Boolean -> String
    def start(self, started):
        self.client_player.tournamnent_start_update()
        return Messages.ACK

    # Informs the player whether they won the tournament
    # Boolean -> String
    def end(self, won):
        self.client_player.tournamnent_result_update(won)
        self.stopped = True
        return Messages.ACK

    # Informs the player of the color they will be playing this game with
    # String -> String
    def playing_as(self, color):
        self.client_player.color_assignment_update(color)
        return Messages.ACK

    # Sets the list of colors that will be present within this game
    # List[String] -> String
    def playing_with(self, colors):
        self.colors = colors
        return Messages.ACK

    # Gives the player the current State of the game.
    # Returns the placement the player decides to make.
    # Formatted-State -> Position
    def setup(self, state):
        internal_state = self.internalize_state(state)
        self.client_player.inital_state_update(internal_state)
        placement = self.client_player.get_placement()
        return placement[1]

    # Gives the player the current State of the game.
    # Returns the move the player decides to make.
    # Formatted-State -> Formatted-Move
    def take_turn(self, state, actions):
        internal_state = self.internalize_state(state)
        self.client_player.inital_state_update(internal_state)
        move = self.client_player.get_move()
        print("Client {} want {} move".format(self.name, move))
        return Messages.convert_action(move)


    # Converts the Formatted-State to a State.
    # Formatted-State -> State
    def internalize_state(self, state):
        board = state["board"]
        player_colors = [player["color"] for player in state["players"]]
        players = []
        for color in self.colors:
            if color in player_colors:
                players.append(color)

        current_player = state["players"][0]
        turn_index = self.colors.index(current_player["color"])

        penguin_positions = {}
        for player in state["players"]:
            position = []
            for pos in player["places"]:
                position.append(tuple(pos))
            penguin_positions[player["color"]] = position

        player_scores = {}
        for player in state["players"]:
            color = player["color"]
            score = player["score"]
            player_scores[color] = score

        internalized_state = (board, players, penguin_positions, turn_index, player_scores)
        print("Client internalized state to ", internalized_state)
        return internalized_state
