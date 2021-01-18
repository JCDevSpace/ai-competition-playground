from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
import asyncio
from Game.Remote.tcp_server_proxy import TCPServerProxy
from Game.Common.util import generate_players


if __name__ == "__main__":
    server_proxy = TCPServerProxy("bestplayer", *generate_players(1, 1))
    asyncio.run(server_proxy.join_tournament())