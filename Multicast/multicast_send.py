"""
Example for UPD multicast sender
"""
import socket

GROUP = "224.1.1.1"
PORT = 5004
# 2-hop restriction in network
TTL = 2
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
sock.sendto(b"hello world", (GROUP, PORT))
