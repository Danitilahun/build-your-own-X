from typing import Dict
from .probe import ProbeSocket


class HopTracer:
    """Handles tracing individual hops."""

    def __init__(self, dest_ip: str, probe_socket: ProbeSocket):
        self.dest_ip = dest_ip
        self.probe_socket = probe_socket

    def trace_hop(self, ttl: int) -> Dict:
        hop_data = {
            'hop': ttl,
            'responses': [],
            'reached_destination': False
        }

        for probe in range(3):
            port = ProbeSocket.UDP_PORT_START + \
                ((ttl - 1) * 3 + probe) % (ProbeSocket.UDP_PORT_END -
                                           ProbeSocket.UDP_PORT_START + 1)
            response = self.probe_socket.send_probe(self.dest_ip, port, ttl)
            hop_data['responses'].append(response)

            if response and response['ip'] == self.dest_ip:
                hop_data['reached_destination'] = True

        return hop_data
