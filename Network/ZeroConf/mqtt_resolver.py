#!/usr/bin/env python3

""" Example of resolving a service with a known name """
import logging
import time
from typing import Any
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf

_infos = []


def _on_service_state_change(
    zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
    """
    on_service_state_change _summary_

    Args:
        zeroconf (Zeroconf): _description_
        service_type (str): _description_
        name (str): _description_
        state_change (ServiceStateChange): _description_
    """
    logging.debug("Service %s of type %s state changed: %s", name, service_type, state_change)

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(type_=service_type, name=name, timeout=1500)
        if info:
            _infos.append(info)


def mdns_service_discovery(service: str = "_mqtt._tcp.local.", timeout: int = 5) -> Any | None:
    """
    service_discovery _summary_

    Args:
        service (str, optional): _description_. Defaults to "_mqtt._tcp.local.".

    Returns:
        Any | None: _description_
    """
    zc = Zeroconf(ip_version=IPVersion.All)
    _ = ServiceBrowser(zc, service, handlers=[_on_service_state_change])
    #    sleep(timeout)
    # enforce the timeout
    timeout = time.time() + timeout
    try:
        while time.time() < timeout:
            # bounce as soon as we have one device
            if len(_infos) > 0:
                break
            time.sleep(0.05)
    except KeyboardInterrupt:  # pragma: no cover
        pass
    finally:
        zc.close()

    results = []
    for info in _infos:
        results.append((info.server, info.port, info.parsed_addresses()))
    return results


if __name__ == "__main__":
    ret = mdns_service_discovery("_mqtt._tcp.local.")

    print(ret)
