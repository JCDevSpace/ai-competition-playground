from pathlib import Path
from sys import path
pwd = Path(__file__).parent.absolute()
path.append(str(pwd / "../../.."))

import unittest
import asyncio
from Game.Remote.tcp_server_proxy import TCPServerProxy
from Game.Common.util import generate_players

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from time import sleep

async def generate_server_proxies(players):
    proxies = []
    for i, player in enumerate(players):
        reader, writer = await asyncio.open_connection(
        "localhost", 1234)
        proxies.append(TCPServerProxy(player, reader, writer))

        name = "player"+str(i)
        writer.write(name.encode())
        await writer.drain()

    return proxies

def runner(proxy):
    asyncio.run(proxy.start_communication())

async def signup(name):
    reader, writer = await asyncio.open_connection(
        "localhost", 1234)

    writer.write(name.encode())
    await writer.drain()
    print("wrote to server", name)
    print("waiting to read from server")
    stuff = await reader.read()
    print("read {} from server", stuff)

# if __name__ == "__main__":
async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 1234)

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client('Hello World!!!!!!!!'))

    