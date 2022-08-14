"""
    minimal upnp discovery example
"""

import re
import sys

# import time
import base64
import struct
import socket
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import requests


###
# Send a multicast message tell all the pnp services that we are looking
# For them. Keep listening for responses until we hit a 3 second timeout (yes,
# this could technically cause an infinite loop). Parse the URL out of the
# 'location' field in the HTTP header and store for later analysis.
#
# @return the set of advertised upnp locations
###
def discover_pnp_locations():
    """
    discover_pnp_locations

    Returns:
        _type_: _description_
    """
    locations = set()
    location_regex = re.compile("location:[ ]*(.+)\r\n", re.IGNORECASE)
    ssdpDiscover = (
        "M-SEARCH * HTTP/1.1\r\n"
        + "HOST: 239.255.255.250:1900\r\n"
        + 'MAN: "ssdp:discover"\r\n'
        + "MX: 1\r\n"
        + "ST: ssdp:all\r\n"
        + "\r\n"
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(ssdpDiscover.encode("ASCII"), ("239.255.255.250", 1900))
    sock.settimeout(3)
    try:
        while True:
            data, addr = sock.recvfrom(2048)  # buffer size is 1024 bytes
            print(f"Received a reply from {addr} with {data}\n")
            location_result = location_regex.search(data.decode("ASCII"))
            if location_result and (not location_result.group(1) in locations):
                locations.add(location_result.group(1))
    except socket.error:
        sock.close()

    return locations


def print_attribute(xml, xml_name, print_name):
    """
    print_attribute Tries to print an element extracted from the XML.

    Args:
        xml (_type_): the xml tree we are working on
        xml_name (_type_): the name of the node we want to pull text from
        print_name (_type_): the name we want to appear in stdout
    """
    try:
        temp = xml.find(xml_name).text
        print(f"\t-> {print_name}: {temp}")
    except AttributeError:
        return

    return


###
#
#
# @param locations
# @return igd_ctr (the control address) and igd_service (the service type)
###
def parse_locations(locations):
    """
    parse_locations Loads the XML at each location and prints out the API along with some other
    interesting data.

    Args:
        locations (_type_): a collection of URLs
    """
    if len(locations) == 0:
        return

    for location in locations:
        print(f"[+] Loading {location}...")
        try:
            resp = requests.get(location, timeout=2)
            if resp.headers.get("server"):
                print("\t-> Server String: %s" % resp.headers.get("server"))
            else:
                print("\t-> No server string")

            parsed = urlparse(location)

            print("\t==== XML Attributes ===")
            try:
                xmlRoot = ET.fromstring(resp.text)
            except:
                print("\t[!] Failed XML parsing of {location}")
                continue

            print_attribute(
                xmlRoot,
                "./{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-upnp-org:device-1-0}deviceType",
                "Device Type",
            )
            print_attribute(
                xmlRoot,
                "./{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-upnp-org:device-1-0}friendlyName",
                "Friendly Name",
            )
            print_attribute(
                xmlRoot,
                "./{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-upnp-org:device-1-0}manufacturer",
                "Manufacturer",
            )
            print_attribute(
                xmlRoot,
                "./{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-upnp-org:device-1-0}manufacturerURL",
                "Manufacturer URL",
            )
            print_attribute(
                xmlRoot,
                "./{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-upnp-org:device-1-0}modelDescription",
                "Model Description",
            )
            print_attribute(
                xmlRoot,
                "./{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-upnp-org:device-1-0}modelName",
                "Model Name",
            )
            print_attribute(
                xmlRoot,
                "./{urn:schemas-upnp-org:device-1-0}device/{urn:schemas-upnp-org:device-1-0}modelNumber",
                "Model Number",
            )

            igd_ctr = ""
            igd_service = ""
            cd_ctr = ""
            cd_service = ""
            wps_ctr = ""
            wps_service = ""

            print("\t-> Services:")
            services = xmlRoot.findall(".//*{urn:schemas-upnp-org:device-1-0}serviceList/")
            for service in services:
                print(
                    "\t\t=> Service Type: %s"
                    % service.find("./{urn:schemas-upnp-org:device-1-0}serviceType").text
                )
                print(
                    "\t\t=> Control: %s"
                    % service.find("./{urn:schemas-upnp-org:device-1-0}controlURL").text
                )
                print(
                    "\t\t=> Events: %s"
                    % service.find("./{urn:schemas-upnp-org:device-1-0}eventSubURL").text
                )

                # Add a lead in '/' if it doesn't exist
                scp = service.find("./{urn:schemas-upnp-org:device-1-0}SCPDURL").text
                if scp[0] != "/":
                    scp = "/" + scp
                serviceURL = parsed.scheme + "://" + parsed.netloc + scp
                print("\t\t=> API: %s" % serviceURL)

                # read in the SCP XML
                resp = requests.get(serviceURL, timeout=2)
                try:
                    serviceXML = ET.fromstring(resp.text)
                except:
                    print("\t\t\t[!] Failed to parse the response XML")
                    continue

                actions = serviceXML.findall(".//*{urn:schemas-upnp-org:service-1-0}action")
                for action in actions:
                    print("\t\t\t- " + action.find("./{urn:schemas-upnp-org:service-1-0}name").text)
                    if (
                        action.find("./{urn:schemas-upnp-org:service-1-0}name").text
                        == "AddPortMapping"
                    ):
                        igd_ctr = (
                            parsed.scheme
                            + "://"
                            + parsed.netloc
                            + service.find("./{urn:schemas-upnp-org:device-1-0}controlURL").text
                        )
                        igd_service = service.find(
                            "./{urn:schemas-upnp-org:device-1-0}serviceType"
                        ).text
                    elif action.find("./{urn:schemas-upnp-org:service-1-0}name").text == "Browse":
                        cd_ctr = (
                            parsed.scheme
                            + "://"
                            + parsed.netloc
                            + service.find("./{urn:schemas-upnp-org:device-1-0}controlURL").text
                        )
                        cd_service = service.find(
                            "./{urn:schemas-upnp-org:device-1-0}serviceType"
                        ).text
                    elif (
                        action.find("./{urn:schemas-upnp-org:service-1-0}name").text
                        == "GetDeviceInfo"
                    ):
                        wps_ctr = (
                            parsed.scheme
                            + "://"
                            + parsed.netloc
                            + service.find("./{urn:schemas-upnp-org:device-1-0}controlURL").text
                        )
                        wps_service = service.find(
                            "./{urn:schemas-upnp-org:device-1-0}serviceType"
                        ).text

            if igd_ctr and igd_service:
                print("\t[+] IGD port mapping available. Looking up current mappings...")
                find_port_mappings(igd_ctr, igd_service)

            if cd_ctr and cd_service:
                print("\t[+] Content browsing available. Looking up base directories...")
                find_directories(cd_ctr, cd_service)

            if wps_ctr and wps_service:
                print("\t[+] M1 available. Looking up device information...")
                find_device_info(wps_ctr, wps_service)

        except requests.exceptions.ConnectionError:
            print("[!] Could not load %s" % location)
        except requests.exceptions.ReadTimeout:
            print("[!] Timeout reading from %s" % location)

    return


def find_port_mappings(p_url, p_service):
    """
    find_port_mappings Finds the currently existing external to internal port mappings. This logic
    assumes that the mappings live in a list we can walk. We give up after we
    reach our first non 200 OK.

    Args:
        p_url (_type_): the url to send the SOAPAction to
        p_service (_type_): the service in charge of this control URI
    """
    index = 0
    while True:
        payload = (
            '<?xml version="1.0" encoding="utf-8" standalone="yes"?>'
            + '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
            + "<s:Body>"
            + '<u:GetGenericPortMappingEntry xmlns:u="'
            + p_service
            + '">'
            + "<NewPortMappingIndex>"
            + str(index)
            + "</NewPortMappingIndex>"
            + "</u:GetGenericPortMappingEntry>"
            + "</s:Body>"
            + "</s:Envelope>"
        )

        soapActionHeader = {
            "Soapaction": '"' + p_service + "#GetGenericPortMappingEntry" + '"',
            "Content-type": 'text/xml;charset="utf-8"',
        }
        resp = requests.post(p_url, data=payload, headers=soapActionHeader)

        if resp.status_code != 200:
            return
        else:
            try:
                xmlRoot = ET.fromstring(resp.text)
            except:
                print("\t\t[!] Failed to parse the response XML")
                return

            externalIP = xmlRoot.find(".//*NewRemoteHost").text
            if externalIP == None:
                externalIP = "*"

            print(
                "\t\t[%s] %s:%s => %s:%s | Desc: %s"
                % (
                    xmlRoot.find(".//*NewProtocol").text,
                    externalIP,
                    xmlRoot.find(".//*NewExternalPort").text,
                    xmlRoot.find(".//*NewInternalClient").text,
                    xmlRoot.find(".//*NewInternalPort").text,
                    xmlRoot.find(".//*NewPortMappingDescription").text,
                )
            )

        index += 1


def find_directories(p_url, p_service):
    """
    find_directories Send a 'Browse' request for the top level directory. We will print out the
    top level containers that we observer. I've limited the count to 10.

    Args:
        p_url (_type_):  the url to send the SOAPAction to
        p_service (_type_): the service in charge of this control URI
    """
    payload = (
        '<?xml version="1.0" encoding="utf-8" standalone="yes"?>'
        + '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
        + "<s:Body>"
        + '<u:Browse xmlns:u="'
        + p_service
        + '">'
        + "<ObjectID>0</ObjectID>"
        + "<BrowseFlag>BrowseDirectChildren</BrowseFlag>"
        + "<Filter>*</Filter>"
        + "<StartingIndex>0</StartingIndex>"
        + "<RequestedCount>40</RequestedCount>"
        + "<SortCriteria></SortCriteria>"
        + "</u:Browse>"
        + "</s:Body>"
        + "</s:Envelope>"
    )

    soapActionHeader = {
        "Soapaction": '"' + p_service + "#Browse" + '"',
        "Content-type": 'text/xml;charset="utf-8"',
    }

    resp = requests.post(p_url, data=payload, headers=soapActionHeader)
    if resp.status_code != 200:
        print(f"\t\tRequest failed with status: {resp.status_code}")
        return

    try:
        xml_root = ET.fromstring(resp.text)
        containers = xml_root.find(".//*Result").text
        if not containers:
            return

        xml_root = ET.fromstring(containers)
        containers = xml_root.findall("./{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}container")
        for container in containers:
            if (
                container.find("./{urn:schemas-upnp-org:metadata-1-0/upnp/}class").text.find(
                    "object.container"
                )
                > -1
            ):
                print(
                    "\t\tStorage Folder: "
                    + container.find("./{http://purl.org/dc/elements/1.1/}title").text
                )
    except:
        print("\t\t[!] Failed to parse the response XML")


def find_device_info(p_url, p_service):
    """
    find_device_info Send a 'GetDeviceInfo' request which gets an 'M1' WPS message in return. This
        message is in a TLV format. We print out some of the types/values.

    Args:
        p_url (_type_): the url to send the SOAPAction to
        p_service (_type_):  the service in charge of this control URI
    """
    payload = (
        '<?xml version="1.0" encoding="utf-8" standalone="yes"?>'
        + '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
        + "<s:Body>"
        + '<u:GetDeviceInfo xmlns:u="'
        + p_service
        + '">'
        + "</u:GetDeviceInfo>"
        + "</s:Body>"
        + "</s:Envelope>"
    )

    soap_action_header = {
        "Soapaction": '"' + p_service + "#GetDeviceInfo" + '"',
        "Content-type": 'text/xml;charset="utf-8"',
    }

    resp = requests.post(p_url, data=payload, headers=soap_action_header)
    if resp.status_code != 200:
        print(f"\t[-] Request failed with status: {resp.status_code}")
        return

    info_regex = re.compile("<NewDeviceInfo>(.+)</NewDeviceInfo>", re.IGNORECASE)
    encoded_info = info_regex.search(resp.text)
    if not encoded_info:
        print("\t[-] Failed to find the device info")
        return

    info = base64.b64decode(encoded_info.group(1))
    while info:
        try:
            _type, length = struct.unpack("!HH", info[:4])
            value = struct.unpack("!%is" % length, info[4 : 4 + length])[0]
            info = info[4 + length :]

            print(f"\t\Raw Type: {hex(_type)}")
            if _type == 0x1023:
                print(f"\t\tModel Name: {value}")
            elif _type == 0x1021:
                print(f"\t\tManufacturer: {value}")
            elif _type == 0x1011:
                print(f"\t\tDevice Name: {value}")
            elif _type == 0x1020:
                pretty_mac = ":".join("%02x" % ord(v) for v in value)
                print(f"\t\tMAC Address: {pretty_mac}")
            elif _type == 0x1032:
                encoded_pk = base64.b64encode(value)
                print(f"\t\tPublic Key: {encoded_pk}")
            elif _type == 0x101A:
                encoded_nonce = base64.b64encode(value)
                print(f"\t\tNonce: {encoded_nonce}")

        except:
            print("Failed TLV parsing")
            break


###
#
###
def main(argv):
    """
    main Discover upnp services on the LAN and print out information needed to
        investigate them further. Also prints out port mapping information if it
        exists

    Args:
        argv (_type_): _description_
    """
    print("[+] Discovering UPnP locations")
    locations = discover_pnp_locations()
    print("[+] Discovery complete")
    print("[+] %d locations found:" % len(locations))
    for location in locations:
        print(f"\t-> {location}")

    parse_locations(locations)

    print("[+] Fin.")


if __name__ == "__main__":
    main(sys.argv)
