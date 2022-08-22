import logging
import time
import socket
from typing import Any
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf, ZeroconfServiceTypes

# "_airplay._tcp.local."
def find_service(service_type, timeout=10, fast=False):
    """Use Zeroconf/MDNS to locate servers on the local network

    Args:
        timeout(int):   The number of seconds to wait for responses.
                        If fast is false, then this function will always block for this number of seconds.
        fast(bool):     If true, do not wait for timeout to expire,
                        return as soon as we've found at least one server

    Returns:
        list:   A list of objects; one for each server found

    """

    # this will be our list of devices
    devices = []

    # zeroconf will call this method when a device is found
    def on_service_state_change(zeroconf, service_type, name, state_change) -> Any | None:
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            if info is None:
                return

            try:
                name, _ = name.split(".", 1)
            except ValueError:
                pass

            # if len(info._ipv6_addresses) > 0:
            # devices.append(socket.inet_ntoa(info._ipv6_addresses[0]), info.port, name)

            # if len(info._ipv4_addresses) > 0:
            #    devices.append((socket.inet_ntoa(info.addresses[0]), info.port, name))

            devices.append(info)

    # search for devices
    try:
        zeroconf = Zeroconf()
        browser = ServiceBrowser(zeroconf, service_type, handlers=[on_service_state_change])  # NOQA
    except NameError:
        logging.warning(
            "find() requires the zeroconf package but it could not be imported. "
            "Install it if you wish to use this method. https://pypi.python.org/pypi/zeroconf",
            stacklevel=2,
        )
        return None

    # enforce the timeout
    timeout = time.time() + timeout
    try:
        while time.time() < timeout:
            # if they asked us to be quick, bounce as soon as we have one device
            if fast and len(devices) > 0:
                break
            time.sleep(0.05)
    except KeyboardInterrupt:  # pragma: no cover
        pass
    finally:
        zeroconf.close()

    return devices


if __name__ == "__main__":
    mqtt_devices = find_service(service_type="_mqtt._tcp.local.", timeout=10, fast=False)
    if len(mqtt_devices) > 0:
        for device in mqtt_devices:
            print(f"Found: {device}")
