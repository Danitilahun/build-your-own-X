from .dns import DNSResolver
from .probe import ProbeSocket
from .hop import HopTracer
from .output import OutputFormatter


class Traceroute:
    """Main traceroute implementation."""

    def __init__(self, hostname: str, max_hops: int = 64, timeout: float = 2.0, packet_size: int = 32):
        self.hostname = hostname
        self.max_hops = max_hops
        self.timeout = timeout
        self.packet_size = packet_size

        payload_text = b'codingchallenges.fyi trace route'
        self.payload = payload_text + b'0' * \
            max(0, packet_size - len(payload_text))

        self.resolver = DNSResolver()
        self.dest_ip = self.resolver.resolve_hostname(hostname)
        self.probe_socket = ProbeSocket(self.payload, timeout)
        self.hop_tracer = HopTracer(self.dest_ip, self.probe_socket)
        self.formatter = OutputFormatter()

        self.UDP_PORT_START = ProbeSocket.UDP_PORT_START
        self.UDP_PORT_END = ProbeSocket.UDP_PORT_END

    def run(self) -> None:
        try:
            self.formatter.print_header(
                self.hostname, self.dest_ip, self.max_hops, self.packet_size)

            for ttl in range(1, self.max_hops + 1):
                hop_result = self.hop_tracer.trace_hop(ttl)
                self.formatter.print_hop(
                    hop_result['hop'], hop_result['responses'], self.resolver)

                if hop_result['reached_destination']:
                    break
        finally:
            self.probe_socket.cleanup()
