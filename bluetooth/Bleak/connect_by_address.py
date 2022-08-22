"""
Connect by BLEDevice
"""

import asyncio
import platform
import sys

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

ADDRESS = (
    "A5:B3:C2:22:15:24" if platform.system() != "Darwin" else "B9EA5233-37EF-4DD6-87A8-2A875E821C46"
)
CHARACTERISTIC_UUID = f"0000{0xFFF4:x}-0000-1000-8000-00805f9b34fb"


async def main(ble_address: str):
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))
