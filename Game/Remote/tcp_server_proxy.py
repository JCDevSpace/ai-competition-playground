from Game.Common.util import safe_execution
from Game.Remote.message import Message, MsgType


class TCPServerProxy:
    """
    A TCPServerProxy is a combination of:
    -Streams.StreamReader:
        a stream reader object to read incoming messages from the server
    -Streams.StreamWriter:
        a stream writer object to write responses to the server
    -IPlayer:
        a client created player that implements the IPlayer interface

    A ServerProxy is a proxy that communicates with the server over tcp, enabling external player implementations to interaction with the game server just like local logical interactions, handling convertion of data between internal representations and json messages as well as sending and recieving these json messages to and from the server.
    """

    def __init__(self, player, reader, writer):
        """Initializes a proxy that interacts with the given player implementation using the given stream reader and writer that allows communication with the server.

        Args:
            player (IPlayer): a player object, client implementation
            reader (StreamReader): a stream reader, from result of open_connection using the Streams module
            writer (StreamWriter): a stream writer, from result of open_connection using the Streams module
        """
        self.player = player
        self.reader = reader
        self.writer = writer

    async def start_communication(self):
        """Starts the asychronus communication with the server.
        """
        message = await self.reader.read()
        print("Recieved {} from server".format(message.decode()))
        response = self.process_message(message)
        if response:
            self.writer.write(response.encode())
            await self.writer.drain()

    def process_message(self, message):
        """Processes the given message and returns the expected response from the corresponding responder, if the given message is an invalid one returns false.

        Args:
            message (json): a json formmated message to be processed

        Returns:
            union(False, X): False when given an invalid message othewise the yield of the corresponding message responder
        """
        msg_type, content = Message.decode(message)

        if msg_type != Message.INVALID:
            handler = self.get_responder(msg_type)
            ret, exc = safe_execution(handler, [content], wait=True)
            if exc:
                print(exc)
            return ret
        return False

    def get_responder(self, msg_type):
        """Finds the player message responder base on the given message type from the lookup table.

        Args:
            msg_type (Message.type): one of the message types specified in Message

        Returns:
            func: a func to be execute in response to the incoming message
        """
        responder_table = {
            MsgType.T_START: self.player.tournament_start_update,
            MsgType.T_PROGRESS: self.player.tournament_progress_update,
            MsgType.T_END: self.player.tournament_end_update,
            MsgType.PLAYING_AS: self.player.playing_as,
            MsgType.T_ACTION: self.player.get_action,
            MsgType.G_STATR: self.player.game_start_update,
            MsgType.G_ACTION: self.player.game_action_update,
            MsgType.G_KICK: self.player.game_kick_update
        }
        return responder_table[msg_type]



