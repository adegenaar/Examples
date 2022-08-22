"""
Disconnect callback
-------------------

An example showing how the `set_disconnected_callback` can be used on BlueZ backend.

Updated on 2019-09-07 by hbldh <henrik.blidh@gmail.com>

"""

import asyncio

from bleak import BleakClient, BleakScanner

ADDRESS = "A5:B3:C2:22:15:24"


async def main():
    # devs = await discover()
    # if not devs:
    #     print("No devices found, try again later.")
    #     return

    disconnected_event = asyncio.Event()

    def disconnected_callback(client):
        print("Disconnected callback called!")
        disconnected_event.set()

    device = await BleakScanner.find_device_by_address(ADDRESS, timeout=20.0)

    async with BleakClient(device, disconnected_callback=disconnected_callback) as client:
        services = await client.get_services()
        print("Services:")
        for service in services:
            print(service)
        print("Sleeping until device disconnects...")
        await disconnected_event.wait()
        print("Connected:", client.is_connected)


if __name__ == "__main__":
    asyncio.run(main())
