"""
Bleak Scanner
-------------
Updated on 2020-08-12 by hbldh <henrik.blidh@nedomkull.com>
"""

import asyncio
import sys

from bleak import BleakScanner


async def main(wanted_name):
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name and d.name.lower() == wanted_name.lower()
    )
    print(device)


if __name__ == "__main__":
    name = "BDM"
    if len(sys.argv) > 1:
        name = sys.argv[1]

    asyncio.run(main(name))
