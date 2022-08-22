""" Example of resolving a service with a known name """

import logging
import sys

from zeroconf import Zeroconf

TYPE = '_tcp.local.'
NAME = '_mqtt'

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # if len(sys.argv) > 1:
    #     assert sys.argv[1:] == ['--debug']
    logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    zeroconf = Zeroconf()

    try:
        print(zeroconf.get_service_info(TYPE, NAME + '.' + TYPE))
    finally:
        zeroconf.close()