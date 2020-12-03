import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(scriptPath / "../.."))

import socket
from Fish.Remote.messages import Messages

ACK = "void"

# Proxy that receives JSON from the remote_player and converts it
# into Python before calling the methods on the client player. Then
# the response from the client is returned to the remote_player.
class Client:

    # Initializes a client that will communicate with the given server on the given port,
    # and the given player.
    # String, Player_Interface, String, Natural, Natural -> Client
    def __init__(self, name, client_player, server_host="localhost", server_port=13452, buff_size=4096):
        self.name = name
        self.client_player

        self.server_host = server_host
        self.server_port = server_port
        self.buff_size = buff_size

        self.stopped = False

    # Starts the client by signing up the player for a tournament with the server
    # then sit and waits for messages from the server and responses correspondingly
    # until the client is stopped
    def run(self):
        if self.tournament_signup():
            self.process_messages()        

    # Stops the client
    def stop(self):
        self.stopped = True
        self.sock.close()

    # Signs the client player up for a tournament with the server
    # and return True else if the connection of signup failed returns
    # False
    def tournament_signup(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_host, self.server_port))
            self.sock.sendall(name)
            return True
        except:
            return False

    # Waits and recives messages from the server and executes the corresponding
    # action for the server request for the the recieved message, 
    # stops receiving messages when the client is stopped.
    def process_messages(self):
        req_handler_table = {
            Messages.START: self.start,
            Messages.END: self.end,
            Messages.PLAYING_AS: self.playing_as,
            Messages.PLAYING_WITH: self.playing_with,
            Messages.SETUP: self.setup,
            Messages.TAKE_TURN: self.take_turn
        }
        
        while not stopped:
            with self.sock.recv(self.buff_size) as req_msg:
                converted_request = Messages.convert_message(req_msg)
                
                if converted_request:
                    req_type = converted_request[0]
                    handler = req_handler_table[req_type]
                    client_response = handler(*converted_request[1])
                    self.sock.sendall(json.dumps(client_response))

    # Informs the player that the tournament has started
    # Boolean -> String
    def start(self, started):
        self.client_player.tournament_start_update()
        return ACK


    # Informs the player whether they won the tournament
    # Boolean -> String
    def end(self, won):
        self.client_player.tournamnent_result_update()
        return ACK


    # Informs the player of the color they will be playing this game with
    # String -> String
    def playing_as(self, color):
        self.client_player.color_assignment_update(color):
        return ACK

    
    # Sets the list of colors that will be present within this game
    # List[String] -> String
    def playing_with(self, colors):
        self.colors = colors
        return ACK


    # Sets up  
    # List[String] -> String
    def setup(self, state):
        board = state["board"]
        players = self.colors
        
        current_player = state["players"][0]
        penguin_positions = current_player["places"]
        turn_index = self.colors.index(current_player["color"])

        player_scores = {}
        for player in state["players"]:
            color = player["color"]
            score = player["score"]
            player_scores[color] = score

        internal_state = (board, players, penguin_positions, turn_index, player_scores)
        self.client_player.inital_state_update(internal_state)
        placement = self.client_player.get_placement()
        return placement[1]
        

    def take_turn(self, state, actions):
        pass
    
    