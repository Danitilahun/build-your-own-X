import socket
import sys


class DNSResolver:
    """Handles DNS resolution for hostnames and reverse IP lookups."""

    @staticmethod
    def resolve_hostname(hostname: str) -> str:
        """Resolve hostname to IP address."""
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            print(f"Error: Cannot resolve hostname '{hostname}'")
            sys.exit(1)

    @staticmethod
    def reverse_lookup(ip: str) -> str:
        """Perform reverse DNS lookup on IP address."""
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname.split('.')[0]
        except (socket.herror, socket.error):
            return ip
