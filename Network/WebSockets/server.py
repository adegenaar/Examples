#!/usr/bin/env python
"""
WebSockets Hello Server
See: https://websockets.readthedocs.io
"""

import asyncio
import websockets


async def echo(websocket):
    """
    echo For every message that is received, echo the message

    Args:
        websocket (_type_): _description_
    """
    async for message in websocket:
        await websocket.send("Hello " + message)


async def main():
    """
    main Main entry point for the application
    """

    async with websockets.serve(echo, host="localhost", port=8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
