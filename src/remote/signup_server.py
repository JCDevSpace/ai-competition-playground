#!/usr/bin/env python3

from src.remote.web_proxy_observer import WebProxyObserver as Observer
from src.remote.tcp_proxy_player import TCPProxyPlayer as Player
from src.admin.manager import Manager
from src.remote.message import MsgType
import src.remote.message as Message

from src.common.util import load_config, generate_players
from asyncio import start_server, create_task, sleep, get_event_loop
from queue import Queue
from time import time

import asyncio
import websockets
import traceback


class SignUpServer:
    """
    A SignUpServer is a combination of:
    -dict:
        a dictionary of configuration parameters loaded on startup
    -Queue:
        a queue to keep track of players who have signed up for a tournament

    A SignUpServer is a tcp_server that accepts signups from both tcp and websocket connections to a board game tournament. A match maker is started once anyone signed up for a tournament waiting for the configured match make length of new players to join, once that match maker length is over, a tournament manager is create and runs a tournament with all the players in the queue filling any open slots with inhouse AI players if less than the minimum players signed up.
    """

    def __init__(self):
        """Initializes a signup tcp_server, ready to start accepting signup and scheduling tournaments either once enough players signed up for a tournament of after a period of time
        """
        self.config = load_config("default_signup.yaml")
        self.player_queue = Queue()
        self.observer_queue = Queue()

    def start(self):
        """Starts the signup tcp_server, processing tournament observer and signups, starts both a tcp and web server to accept communication from the two different protocols.
        """
        loop = get_event_loop()

        tcp_server = loop.run_until_complete(start_server(self.process_tcp_signup, self.config["host"], self.config["tcp_port"]))
        web_server = loop.run_until_complete(websockets.serve(self.process_web_signup, self.config["host"], self.config["web_port"]))

        addr = tcp_server.sockets[0].getsockname()
        print(f'TCP serving on {addr}')
        addr = web_server.sockets[0].getsockname()
        print(f'Web serving on {addr}')

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        tcp_server.close()
        web_server.close()
        loop.run_until_complete(tcp_server.wait_closed())
        loop.run_until_complete(web_server.wait_closed())
        loop.close()

    async def process_tcp_signup(self, reader, writer):
        """Processes a signup request, recieving a name from the client to signup in a tournament with, starts a match maker if the signed up player is the first.

        Args:
            reader (Streams.StreamReader): a reader stream to recieve messages from the client
            writer (Streams.StreamWriter): a writer stream to sent message to the client
        """
        try:
            msg = await reader.read(self.config["read"])
            msg_type, name = Message.decode(msg)

            if msg_type == MsgType.SIGNUP and self.valid_name(name):
                self.player_queue.put(Player(name, 100, reader, writer))
                if self.player_queue.qsize() == 1:
                    create_task(self.match_maker())

        except Exception:
            print(traceback.format_exc())
            writer.close()
            await writer.wait_closed()

    async def process_web_signup(self, websocket, path):
        """Process a web sign up request, recieving a name from the client to signup in a tournament with.

        Args:
            websocket (WebSocket): a websocket to communicate with the client
            path (path): path of the request endpoint
        """
        try:
            msg = await websocket.recv()
            msg_type, name = Message.decode(msg)

            if msg_type == MsgType.OBSERVE and self.valid_name(name):
                web_observer = Observer(name, 200, websocket)
                self.observer_queue.put(web_observer)
                create_task(self.match_maker())
                await web_observer.maintain_com()

        except Exception:
            print(traceback.format_exc())
            await websocket.close()
            await websocket.wait_closed()

    async def match_maker(self):
        """Performs match making by waiting for the match make length of seconds specified in the tcp_server configuration, then after that wait, start a tournament with all the enrolled players and observers.
        """
        enrolled_players = []
        enrolled_observers = []

        start = time()
        while (time() - start) < self.config["match_make"]:
            if self.player_queue.qsize() > 0:
                enrolled_players.append(self.player_queue.get())
            if self.observer_queue.qsize() > 0:
                player = self.observer_queue.get()
                print("Enrolling observer", player.get_id())
                enrolled_observers.append(player)
            await sleep(self.config["rate"])
        
        create_task(self.start_tournament(enrolled_players, enrolled_observers))

    def valid_name(self, name):
        """Determin whether the given name is valid according to the tcp_server configuration requirements.

        Args:
            name (str): a name string

        Returns:
            bool: a boolean with true indicating it's valid
        """
        return len(name) > self.config["min_name"] \
                and len(name) < self.config["max_name"]

    async def start_tournament(self, enrolled_players, enrolled_observers):
        """Starts a board game tournament with the given number of enrolled players and observers, if the enroll number of players is less than the minimum number of players required for a tournament, generates inhouse AI players to fill up the difference.

        Args:
            enrolled_players (list): a list of player object
            enroller_players (list): a list of observer object
        """
        if len(enrolled_players) < self.config["min_players"]:
            enrolled_players.extend( \
                generate_players( \
                    self.config["min_players"] - len(enrolled_players), \
                    self.config["ai_depth"]
                )
            )
        tournament_manager = Manager(enrolled_players, enrolled_observers)
        results = await tournament_manager.run_tournament()
        self.output_results(results)

    def output_results(self, results):
        print("\n\nTournament Results")
        for i, category in enumerate(["Winners:", "Loser:", "Kicked:"]):
            print("")
            print(category)
            for player in results[i]:
                print(player.get_name())
        

if __name__=="__main__":
    server = SignUpServer()
    server.start()