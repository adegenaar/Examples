import asyncio
from bleak import BleakScanner

# https://bleak.readthedocs.io/


def detection_callback(device, advertisement_data):
    print(device.address, "RSSI:", device.rssi, advertisement_data)


async def main():
    scanner = BleakScanner(detection_callback)
    await scanner.start()
    await asyncio.sleep(5.0)
    await scanner.stop()

    for d in scanner.discovered_devices:
        print(d)


asyncio.run(main())


# A8:6B:AD:16:3D:06 RSSI: -82 AdvertisementData(manufacturer_data={76: b'\x02\x15Pv\\\xb7\xd9\xeaN!\x99\xa4\xfa\x87\x96\x13\xa4\x92(L\x85\x9b\xce'})
# A8:6B:AD:16:3D:06 RSSI: -78 AdvertisementData(manufacturer_data={76: b'\x02\x15Pv\\\xb7\xd9\xeaN!\x99\xa4\xfa\x87\x96\x13\xa4\x92(L\x85\x9b\xce'})
# A8:6B:AD:16:3D:06 RSSI: -78 AdvertisementData(manufacturer_data={301: b'\x02\x00\x01\x10\x82\xf0@v\xbe\xeeLT\xac\xdf\x8bo\xf9\xe8*\x90\xc3\xaa\x85K\x96o'})
# A8:6B:AD:16:3D:06 RSSI: -48 AdvertisementData(manufacturer_data={301: b'\x02\x00\x01\x10\x82\xf0@v\xbe\xeeLT\xac\xdf\x8bo\xf9\xe8*\x90\xc3\xaa\x85K\x96o'})
# A8:6B:AD:16:3D:06 RSSI: -48 AdvertisementData(manufacturer_data={76: b'\x02\x15Pv\\\xb7\xd9\xeaN!\x99\xa4\xfa\x87\x96\x13\xa4\x92(L\x85\x9b\xce'})
# A8:6B:AD:16:3D:06 RSSI: -72 AdvertisementData(manufacturer_data={76: b'\x02\x15Pv\\\xb7\xd9\xeaN!\x99\xa4\xfa\x87\x96\x13\xa4\x92(L\x85\x9b\xce'})
# FA:B1:A9:57:5B:BA RSSI: -58 AdvertisementData(local_name='N05Q3', service_uuids=['0000feaf-0000-1000-8000-00805f9b34fb'])
# FA:B1:A9:57:5B:BA RSSI: -58 AdvertisementData(local_name='N05Q3', service_data={'0000feaf-0000-1000-8000-00805f9b34fb': b'\x10\x01\x00\x02Z#\t\x00q\xda4\x00\x000\xb4\x18\x00'}, service_uuids=['0000feaf-0000-1000-8000-00805f9b34fb'])
# 07:D2:F3:8D:F1:8E RSSI: -58 AdvertisementData(manufacturer_data={6: b'\x01\t \x02R\xffZ\xdb\xeb\xcbP\x94gdYX\x1c\x86\x95F\xa74?\x1f\x95B\x99'})
# B8:78:2E:23:2B:B0 RSSI: -66 AdvertisementData(manufacturer_data={76: b'\t\x06\x03\x0b\xc0\xa8\x00v'})
# 07:D2:F3:8D:F1:8E RSSI: -68 AdvertisementData(manufacturer_data={6: b'\x01\t \x02R\xffZ\xdb\xeb\xcbP\x94gdYX\x1c\x86\x95F\xa74?\x1f\x95B\x99'})
# 4C:C9:5E:42:AC:F1 RSSI: -82 AdvertisementData(manufacturer_data={117: b'B\x04\x01\x01vL\xc9^B\xac\xf1N\xc9^B\xac\xf0\x01\xa9\xcf\x00\x00\x00\x00'})
# A8:6B:AD:16:3D:06 RSSI: -72 AdvertisementData(manufacturer_data={301: b'\x02\x00\x01\x10\x82\xf0@v\xbe\xeeLT\xac\xdf\x8bo\xf9\xe8*\x90\xc3\xaa\x85K\x96o'})
# A8:6B:AD:16:3D:06 RSSI: -48 AdvertisementData(manufacturer_data={301: b'\x02\x00\x01\x10\x82\xf0@v\xbe\xeeLT\xac\xdf\x8bo\xf9\xe8*\x90\xc3\xaa\x85K\x96o'})
# A8:6B:AD:16:3D:06 RSSI: -48 AdvertisementData(manufacturer_data={76: b'\x02\x15Pv\\\xb7\xd9\xeaN!\x99\xa4\xfa\x87\x96\x13\xa4\x92(L\x85\x9b\xce'})
# B8:78:2E:23:2B:B0 RSSI: -62 AdvertisementData(manufacturer_data={76: b'\t\x06\x03\x0b\xc0\xa8\x00v'})
# B8:78:2E:23:2B:B0 RSSI: -62 AdvertisementData(manufacturer_data={76: b'\t\x06\x03\x0b\xc0\xa8\x00v'})
# 07:D2:F3:8D:F1:8E RSSI: -62 AdvertisementData(manufacturer_data={6: b'\x01\t \x02R\xffZ\xdb\xeb\xcbP\x94gdYX\x1c\x86\x95F\xa74?\x1f\x95B\x99'})
# FA:B1:A9:57:5B:BA RSSI: -58 AdvertisementData(local_name='N05Q3', service_data={'0000feaf-0000-1000-8000-00805f9b34fb': b'\x10\x01\x00\x02Z#\t\x00q\xda4\x00\x000\xb4\x18\x00'}, service_uuids=['0000feaf-0000-1000-8000-00805f9b34fb'])
# FA:B1:A9:57:5B:BA RSSI: -60 AdvertisementData(local_name='N05Q3', service_data={'0000feaf-0000-1000-8000-00805f9b34fb': b'\x10\x01\x00\x02Z#\t\x00q\xda4\x00\x000\xb4\x18\x00'}, service_uuids=['0000feaf-0000-1000-8000-00805f9b34fb'])
# A8:6B:AD:16:3D:06: Apple, Inc. (b'\x02\x15Pv\\\xb7\xd9\xeaN!\x99\xa4\xfa\x87\x96\x13\xa4\x92(L\x85\x9b\xce')
# FA:B1:A9:57:5B:BA: N05Q3
# 07:D2:F3:8D:F1:8E: Microsoft (b'\x01\t \x02R\xffZ\xdb\xeb\xcbP\x94gdYX\x1c\x86\x95F\xa74?\x1f\x95B\x99')
# B8:78:2E:23:2B:B0: Apple, Inc. (b'\t\x06\x03\x0b\xc0\xa8\x00v')
# 4C:C9:5E:42:AC:F1: Samsung Electronics Co. Ltd. (b'B\x04\x01\x01vL\xc9^B\xac\xf1N\xc9^B\xac\xf0\x01\xa9\xcf\x00\x00\x00\x00')
