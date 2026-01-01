from typing import Optional, Dict, Sequence, Any
from .dns import DNSResolver


class OutputFormatter:
    """Handles formatting and printing of traceroute output."""

    @staticmethod
    def print_header(hostname: str, dest_ip: str, max_hops: int, packet_size: int) -> None:
        print(
            f"traceroute to {hostname} ({dest_ip}), {max_hops} hops max, {packet_size} byte packets")

    @staticmethod
    def print_hop(hop_num: int, responses: Sequence[Optional[Dict[str, Any]]], resolver: DNSResolver) -> None:
        if not responses or not any(r is not None for r in responses):
            print(f"{hop_num} *  * *")
            return

        seen_ips = {}
        for response in responses:
            if response:
                ip = response['ip']
                if ip not in seen_ips:
                    seen_ips[ip] = response
            else:
                if None not in seen_ips:
                    seen_ips[None] = None

        output = f"{hop_num} "
        parts = []

        for ip, response in seen_ips.items():
            if response is None:
                parts.append("*")
            else:
                hostname = resolver.reverse_lookup(ip)
                rtt = response['rtt_ms']

                if hostname and hostname != ip:
                    parts.append(f"{hostname} ({ip}) {rtt:.3f} ms")
                else:
                    parts.append(f"{ip} {rtt:.3f} ms")

        output += "  ".join(parts)
        print(output)