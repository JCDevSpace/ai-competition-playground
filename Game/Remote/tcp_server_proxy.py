from Game.Common.util import safe_execution
from Game.Remote.message import MsgType
import Game.Remote.message as Message
import asyncio

import traceback


class TCPServerProxy:
    """
    A TCPServerProxy is a combination of:
    -Streams.StreamReader:
        a stream reader object to read incoming messages from the server
    -Streams.StreamWriter:
        a stream writer object to write responses to the server
    -dict:
        a dictionary of responder functions with members of MsgType enum as keys a the corresponding function object extracted from a player as value to handle processing message from the server and provide respondes if one is needed

    A ServerProxy is a proxy that communicates with the server over tcp, enabling external player implementations to interaction with the game server just like local logical interactions, handling convertion of data between internal representations and json messages as well as sending and recieving these json messages to and from the server.
    """

    def __init__(self, name, player, host="localhost", port=1234):
        """Initializes a proxy to join a board game tournament that interacts with the given player implementation through a stream reader over a tcp connection.

        Args:
            name (str): a string name to sent the server when joining a tournament
            player (IPlayer): a player object, client implementation
        """
        self.name = name
        self.player = player
        self.host = host
        self.port = port

        self.responder_table = self.setup_responders(player)

    def setup_responders(self, player):
        """Sets up the message responder function lookup table by consuming the given player, the lookup table is setup with members of MsgType enum as keys and the correponding responder function object as values.

        Args:
            player (IPlayer): a player object to abstract responder functions

        Returns:
            dict: a dictionary of the responder table
        """
        return {
            MsgType.T_START: player.tournament_start_update,
            MsgType.T_PROGRESS: player.tournament_progress_update,
            MsgType.T_END: player.tournament_end_update,
            MsgType.PLAYING_AS: player.playing_as,
            MsgType.T_ACTION: player.get_action,
            MsgType.G_START: player.game_start_update,
            MsgType.G_ACTION: player.game_action_update,
            MsgType.G_KICK: player.game_kick_update
        }

    async def join_tournament(self):
        """Joins a board game tournament by signing up with the server and maintaining communication as specified by the plug and play protocol.
        """
        ret = await self.signup()
        if ret:
            await self.communication_loop(*ret)

    async def signup(self):
        """Signs up to a board game tournament with the server by sending it the player name, returns the stream reader and writer for communication with server on successful signup else returns False incidating the signup failed.

        Returns:
            union(tuple, False): a tuple with the first a stream reader and second or False
        """
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            msg = Message.construct_msg(MsgType.SIGNUP, self.name)
            writer.write(msg.encode())
            await writer.drain()

            # msg = await reader.read(100)
            # resp = self.process_message(msg)
            # if resp:
            return reader, writer
        except Exception:
            writer.close()
            await writer.wait_closed()
            print("Encounter problem when signing up", traceback.format_exc())
        return False

    async def communication_loop(self, reader, writer):
        """Runs the communication loop, sending and recieving messeages to and from the server as specified by the plug and play protocol using the given stream reader and writer, the communication can be stopped by setting the stop_communication class instance variable to true.

        Args:
            reader (Streams.StreamReader): a stream reader
            writer (Streams.StreamWriter): a stream writer
        """
        self.stop_communication = False
        while not self.stop_communication and not reader.at_eof():
            msg = await reader.read(1024)
            resp = self.process_message(msg)
            if resp:
                msg = Message(MsgType.G_ACTION, resp)
                writer.write(msg.encode())
                await writer.drain()
        writer.close()
        await writer.wait_closed()

    def process_message(self, message):
        """Processes the given message and returns the expected response from the corresponding responder, if the given message is an invalid one returns false.

        Args:
            message (json): a json formmated message to be processed

        Returns:
            union(False, X): False when given an invalid message othewise the yield of the corresponding message responder
        """
        try:
            msg_type, content = Message.decode(message)

            if msg_type.is_valid():
                handler = self.responder_table[msg_type]
                need_waiting = (msg_type == MsgType.T_ACTION)
                return safe_execution(handler, [content], wait=need_waiting)
        except Exception:
            print(traceback.format_exc())

        return False



