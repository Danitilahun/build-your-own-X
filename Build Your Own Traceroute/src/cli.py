import argparse
from .traceroute import Traceroute


def main():
    parser = argparse.ArgumentParser(
        description="""A simple tool to learn how to create Traceroute.
                    Traceroute is a tool that allows us to trace the route network packets 
                    will take from one computer to another over a network."""
    )

    parser.add_argument('hostname', help="Hostname or IP address to trace to.")
    parser.add_argument('--max-hops', type=int, default=64,
                        help="Maximum number of hops (default: 64)")
    parser.add_argument('--timeout', type=float, default=2.0,
                        help="Timeout per hop in seconds (default: 2.0)")

    args = parser.parse_args()

    tracer = Traceroute(
        args.hostname, max_hops=args.max_hops, timeout=args.timeout)
    tracer.run()


if __name__ == "__main__":
    main()
