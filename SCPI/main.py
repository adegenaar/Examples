""" SCPI demonstration """
# may need zadig for the usb interface if the instrument doesn't show up in the device list

# import time  # for sleep
# import signal  # for ctrl-c
# import sys  # for ping
import os  # for exit signal
import pyvisa  # for SCPI

#import libusb
#import usb.core
import libusb_package

# libusb.config(LIBUSB="libusb C shared library absolute path")
# or
#libusb.config(LIBUSB=None)  # included libusb-X.X.* will be used


# from distutils.sysconfig import get_python_lib
# print(get_python_lib())

# import site
# print(site.getsitepackages())

os.environ["PYUSB_DEBUG"] = "debug"
os.environ["LIBUSB_DEBUG"] = "4"

pyvisa.log_to_screen()

print("PyVisa Resources (default):")
rm = pyvisa.ResourceManager()
for dev in rm.list_resources("?*::INSTR"):
    print("------------")
    print(dev)    

print("PyVisa Resources (@py):")
rm = pyvisa.ResourceManager('@py')
for dev in rm.list_resources("?*::INSTR"):
    print("------------")
    print(dev)    

print("USB Core Resources:")
for dev in libusb_package.find(find_all=True):
    print("------------")
    print(dev)

print("USB Core Resources:")
be = libusb_package.get_libusb1_backend()
if be:
    for dev in libusb_package.find(find_all=True, backend=be):
        print("------------")
        print(dev)

# inst = rm.open_resource('')
# #inst.read_termination = '\r\n'
# #inst.write_termination = '\r\n'

# inst.query_delay = 0.001
# print(inst.query("*IDN"))


# github:
# pklaus / ds1054z
# sam210723 / wavebin
# jbtronics / DS1054_BodePlotter
# charkster / rigol_ds1054z
# vizkoze / DS1054_BodePlotter
