import asyncio
import websockets

async def producer_handler(websocket, path):
    count = 0
    while True:
        msg = await websocket.recv()
        print(f"Recived {msg}")
        if msg == "Bye server!":
            break
        reply = await construct_reply(count)
        count += 1
        await websocket.send(reply)
    await websocket.close(reason="Recieved bye from client")

async def construct_reply(count):
    return f"Reply #{count} from server!!!"

async def communicator(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name} from server!"

    await websocket.send(greeting)

    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

start_server = websockets.serve(communicator, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()