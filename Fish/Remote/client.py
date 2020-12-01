import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()


class Client:

    def __init__(self, client_player):
        self.client_player


    # Starts the client
    def start(self):
        self.recieve_messages()

    # Stops the client
    def stop(self):
        pass

    def tournament_signup(self, name):
        pass

    # Waits and recives messages from the server and executes the corresponding
    # action for the server request for the the recieved message, 
    # stops receiving messages when the client is stopped.
    def receive_messages(self):
        pass