from src.common.i_observer import IObserver
from src.remote.message import MsgType
import src.remote.message as Message
from asyncio import sleep


class WebProxyObserver(IObserver):
    """
    A WebProxyObserver is a combination of:
    -str:
        a string of at most 12 alphanumeric chars for the name of the player
    -id:
        a int that unqiuely identifies the player in the system
    -socket:
        a web socket to sent and receive information from the connectted observer

    A WebProxyObserver is a proxy for external observers to recieve game and tournament updates from the server through a specified plug & play protocal. This allows the referee and tournament manager from the internal server to interaction with observers implemented externally as if it was an in house observer over a network connection.

    A WebProxyObserver implements and IObserver interface.
    """

    def __init__(self, name, unique_id, socket):
        """Initializes a proxy observer connected through a web socket, acts as the proxy for remote observers to recieve updates from the referee as if it's a local observer. 

        Args:
            name (str): a string of the player name
            unique_id (int): a non negative integer that uniquely identifies the client in the system
            socket (WebSocket): a web socket use for communication with client
        """
        self.name = name
        self.id = unique_id
        self.socket = socket

    async def maintain_com(self):      
        """Maintains communication with the web client so the connection doesn't get closed. Shutdowns on reply connection close request from client or close com method is called.
        """
        self.keep_com = True
        while self.keep_com and self.socket.open:
            await sleep(5)
        await self.socket.close()
        await self.socket.wait_closed()

    def close_com(self):
        self.keep_com = False

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    async def game_start_update(self, game_state):
        """Updates the observer on the start of a board game by consuming the given starting players and the game state.

        Args:
            game_state (IState): a game state object
        """
        msg = Message.construct_msg(MsgType.G_START, game_state.serialize())
        await self.socket.send(msg)

    async def game_action_update(self, action, game_state):
        """Updates the observer on an action progress of a board game.

        Args:
            action (Action): an action
            game_state (IState): a game state object
        """
        msg = Message.construct_msg(MsgType.G_ACTION, [action, game_state.serialize()])
        await self.socket.send(msg)

    async def game_kick_update(self, player):
        """Updates the observer on a player kick from the board game.

        Args:
            player (str): a color string representing a player
        """
        msg = Message.construct_msg(MsgType.G_KICK, player)
        await self.socket.send(msg)
    
    async def tournament_start_update(self, players):
        """Updatest the observer on the start of a board game tournament with the initial contestents.

        Args:
            players (list(str)): a list of string representing player names
        """
        msg = Message.construct_msg(MsgType.T_START, players)
        await self.socket.send(msg)

    async def tournament_progress_update(self, match_ups):
        """Updates the observer on the progress of a board game tournament by consuming the given players who advanced to the next round and the players who got knocked out.

        Args:
            match_ups (list): a lisg of list of player names where each list is the group of players in a match.
        """
        msg = Message.construct_msg(MsgType.T_PROGRESS, match_ups)
        await self.socket.send(msg)

    async def tournament_end_update(self, winners):
        """Updates the observer on the final winners of the board game tournament, the finals winners include the top three players, with first player in the winners list as first place and the last one as thrid place. 

        Args:
            winners (list(str)): a list of player names
        """
        msg = Message.construct_msg(MsgType.T_END, winners)
        await self.socket.send(msg)

        self.close_com()