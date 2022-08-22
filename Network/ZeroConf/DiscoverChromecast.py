"""
    Find Google Chromecasts on the local network
"""

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
from zeroconf import ZeroconfServiceTypes


class HttpListener(ServiceListener):
    """
    CastListener A ZeroConf listener for the Google Chromecasts
    """

    def __init__(self) -> None:
        self._service_name = "_http._tcp.local."

    @property
    def service_name(self) -> str:
        """
        service_name Name of the service

        Returns:
            str: predefined name of the service
        """
        return self._service_name

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated\n")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed\n")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print(f"Service {name} added, service info: {info}\n")


class CastListener(ServiceListener):
    """
    CastListener A ZeroConf listener for the Google Chromecasts
    """

    def __init__(self) -> None:
        self._service_name = "_googlecast._tcp.local."

    @property
    def service_name(self) -> str:
        """
        service_name Name of the service

        Returns:
            str: predefined name of the service
        """
        return self._service_name

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated\n")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed\n")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print(f"Service {name} added, service info: {info}\n")


def start_discovery(callback: ServiceListener):
    """
    Start discovering chromecasts on the network.

    This method will start discovering chromecasts on a separate thread. When
    a chromecast is discovered, the callback will be called with the
    discovered chromecast's zeroconf name. This is the dictionary key to find
    the chromecast metadata in listener.services.

    This method returns the CastListener object and the zeroconf ServiceBrowser
    object. The CastListener object will contain information for the discovered
    chromecasts. To stop discovery, call the stop_discovery method with the
    ServiceBrowser object.
    """
    listener = callback()
    return listener, ServiceBrowser(Zeroconf(), listener.service_name, listener)


def main():
    """
    main Entry point for the application
    """
    # print("\n".join(ZeroconfServiceTypes.find()))
    # print("\n")

    zeroconf = Zeroconf()

    start_discovery(CastListener)
    try:
        input("Press enter to exit...\n\n")
    finally:
        zeroconf.close()

    zeroconf = Zeroconf()
    start_discovery(HttpListener)
    try:
        input("Press enter to exit...\n\n")
    finally:
        zeroconf.close()


if __name__ == "__main__":
    main()
