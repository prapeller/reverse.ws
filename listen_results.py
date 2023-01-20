import asyncio

import websockets


async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(f'reversed message: {message}')


async def main():
    url = 'ws://127.0.0.1:5007/ws'
    try:
        async with websockets.connect(url) as ws:
            await handler(ws)
            await asyncio.Future()
    except ConnectionRefusedError:
        print('run command "make build" to run services')

if __name__ == "__main__":
    asyncio.run(main())
