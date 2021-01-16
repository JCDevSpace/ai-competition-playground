from Game.Common.util import load_config, generate_players
from queue import Queue
from asyncio import start_server, create_task
from Game.Remote.tcp_proxy_player import TCPProxyPlayer as Player
from Game.Admin.manager import Manager
from time import sleep

class SignUpServer:
    """

    A SignUpServer is a server that accepts sign-ups to board game tournaments. If a minimum number of players signed up it creates a tournament manager that runs the tournament. It closes itself when it is finished.
    """

    def __init__(self):
        self.config = load_config("default_signup.yaml")
        self.player_queue = Queue()

    async def start(self):
        server = await start_server(
        self.accept_signup_cb, '127.0.0.1', 8888)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

        # self.server = await start_server(self.accept_signup_cb, self.config["host"], self.config["port"])

        # addr = self.server.sockets[0].getsockname()
        # print(f'Serving on {addr}')

        # create_task(self.tournament_scheduler())

        # async with self.server:
        #     await self.server.serve_forever()

    async def accept_signup_cb(self, reader, writer):
        print("Got signup")
        name = await reader.read()
        name = name.decode()
        print("recived name", name)
        print("name is valid", self.valid_name(name))
        if self.valid_name(name):
            print("Signed up", name)
            self.player_queue.put(Player(name, 0, reader, writer))
        else:
            writer.write("Invalid name")
            await writer.drain()

        if self.player_queue.qsize() >= self.config["max_signups"]:
            create_task(start_tournament())     

    async def tournament_scheduler(self):
        while self.server.is_serving():
            sleep(self.config["signup_length"])

            if self.player_queue.qsize() >= self.config["min_signups"]:
                print("Got the minimum number of player, starting tournament")
                create_task(start_tournament())
            print("Don't have enough player currently at", self.player_queue.qsize())

    def valid_name(self, name):
        try:
            return len(name) > self.config["min_name_length"] \
                        and len(name) < self.config["max_name_length"]
        except Exception as e:
            print(e)
        return False

    async def start_tournament(self):
        enrolled_players = []

        while len(enrolled_players) < self.config["max_signup"] \
                and self.player_queue.qsize() > 0:

            enrolled_players.append(self.player_queue.get())

        if len(enrolled_players) < self.config["max_signup"]:
            enrolled_players.extend(generate_players(self.config["max_signup"] - len(enrolled_players), 1))

        tournament_manager = Manager(enrolled_players)

        results = tournament_manager.run_tournament()
        
        print("Tournament Results")
        for i, category in enumerate(["Winners:", "Loser:", "Kicked:"]):
            print(category)
            for player in results[i]:
                print(player.get_name())
        


