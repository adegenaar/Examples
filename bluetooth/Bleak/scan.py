import asyncio
from bleak import BleakScanner


async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)


asyncio.run(main())

# Results from the scan
# 03:F7:18:DE:CE:0A: Microsoft (b'\x01\t \x02\xdbTY\x8aE-\x89, \x9bM\xd7\x874\x01\x17\x1b5\xe8\xda\xf5\xc8B')
# FC:F1:36:AC:C8:AF: Samsung Electronics Co. Ltd. (b'B\x04\x01\x80\xa0\xfc\xf16\xac\xc8\xaf\xfe\xf16\xac\xc8\xae\x01\x00\x00\x00\x00\x00\x00')
# A8:6B:AD:16:3D:06: Apple, Inc. (b'\x02\x15Pv\\\xb7\xd9\xeaN!\x99\xa4\xfa\x87\x96\x13\xa4\x92(L\x85\x9b\xce')
# 4C:C9:5E:42:AC:F1: Samsung Electronics Co. Ltd. (b'B\x04\x01 v \r\x00\x02\x017\x01\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00')
# B8:78:2E:23:2B:B0: Apple, Inc. (b'\t\x06\x03\x0b\xc0\xa8\x00v')
