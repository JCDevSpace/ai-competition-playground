from src.remote.message import MsgType
import src.remote.message as Message


class WebProxyObserver:
    """
    A WebProxyObserver is a combination of:
    -socket:
        a web socket to sent and receive information from the connectted observer
    -str:
        a string of at most 12 alphanumeric chars for the name of the player
    -id:
        a int that unqiuely identifies the player in the system

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

######################Update below##############################

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
        self.writer.write(msg.encode())
        await self.writer.drain()

    async def game_action_update(self, action):
        """Updates the observer on an action progress of a board game.

        Args:
            action (Action): an action
        """
        msg = Message.construct_msg(MsgType.G_ACTION, action)
        self.writer.write(msg.encode())
        await self.writer.drain()

    async def game_kick_update(self, player):
        """Updates the observer on a player kick from the board game.

        Args:
            player (str): a color string representing a player
        """
        if self.color == player:
            self.writer.close()
            await self.writer.wait_closed()
        else:
            msg = Message.construct_msg(MsgType.G_KICK, player)
            self.writer.write(msg.encode())
            await self.writer.drain()
    
    async def tournament_start_update(self, players):
        """Updatest the observer on the start of a board game tournament with the initial contestents.

        Args:
            players (list(str)): a list of string representing player names
        """
        msg = Message.construct_msg(MsgType.T_START, players)
        self.writer.write(msg.encode())
        await self.writer.drain()

    async def tournament_progress_update(self, round_result):
        """Updates the observer on the progress of a board game tournament by consuming the given players who advanced to the next round and the players who got knocked out.

        Args:
            round_result (tuple): a tuple of list of player names where the first are the players who advanced and second players who got knocked out
        """
        msg = Message.construct_msg(MsgType.T_PROGRESS, round_result)
        self.writer.write(msg.encode())
        await self.writer.drain()

    async def tournament_end_update(self, winners):
        """Updates the observer on the final winners of the board game tournament, the finals winners include the top three players, with first player in the winners list as first place and the last one as thrid place. 

        Args:
            winners (list(str)): a list of player names
        """
        msg = Message.construct_msg(MsgType.T_END, winners)
        self.writer.write(msg.encode())

        self.writer.close()
        await self.writer.wait_closed()

    async def playing_as(self, color):
        """Updates the player the color that it's playing as in a board game.

        Args:
            color (str): a color string
        """
        self.color = color

        msg = Message.construct_msg(MsgType.PLAYING_AS, color)
        self.writer.write(msg.encode())
        await self.writer.drain()

    async def get_action(self, game_state):
        """Finds the action to take in a board game by consuming the given game state, the player also recieves all action and player kick updates due to being an observer, thus a stateful implementation is also viable.

        Args:
            game_state (IState): a game state object

        Returns:
            Action: an action to take
        """
        msg = Message.construct_msg(MsgType.T_ACTION, game_state.serialize())
        self.writer.write(msg.encode())
        await self.writer.drain()
        resp = await self.reader.read(1024)
        _, content = Message.decode(resp)
        return content