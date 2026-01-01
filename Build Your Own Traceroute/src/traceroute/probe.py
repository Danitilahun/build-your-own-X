import socket
import time
from typing import Optional, Dict


class ProbeSocket:
    """Manages socket creation and probe packet operations."""

    # ICMP types
    ICMP_ECHO_REQUEST = 8
    ICMP_ECHO_REPLY = 0
    ICMP_TIME_EXCEEDED = 11

    # UDP port range for traceroute
    UDP_PORT_START = 33434
    UDP_PORT_END = 33534

    def __init__(self, payload: bytes, timeout: float = 2.0):
        self.payload = payload
        self.timeout = timeout
        self.icmp_socket = None

    def _create_icmp_socket(self) -> socket.socket:
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(self.timeout)
        return sock

    def send_probe(self, dest_ip: str, port: int, ttl: int) -> Optional[Dict]:
        if self.icmp_socket is None:
            self.icmp_socket = self._create_icmp_socket()

        try:
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

            send_time = time.time()
            udp_socket.sendto(self.payload, (dest_ip, port))
            udp_socket.close()

            try:
                data, addr = self.icmp_socket.recvfrom(512)
                recv_time = time.time()
                rtt_ms = (recv_time - send_time) * 1000

                return {
                    'ip': addr[0],
                    'rtt_ms': rtt_ms,
                    'icmp_type': data[20]
                }
            except socket.timeout:
                return None

        except Exception:
            return None

    def cleanup(self):
        if self.icmp_socket:
            self.icmp_socket.close()
