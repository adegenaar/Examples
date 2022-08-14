#!/usr/bin/env python
"""
WebSockets client example
See: https://websockets.readthedocs.io
"""

import asyncio
import websockets


async def hello():
    """
    hello
    """
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


if __name__ == "__main__":
    asyncio.run(hello())
