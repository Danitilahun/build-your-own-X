import argparse
from .utils import json_or_string
from .client import HTTPClient

def main():
    parser = argparse.ArgumentParser(
        description="A simple tool to learn how to command line tool.")

    parser.add_argument(
        "-X", "--request",
        dest="method",
        default="GET",
        choices=["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"],
        help="Specify a custom request method to use (e.g., GET, POST, DELETE)."
    )

    parser.add_argument(
        "-v", '--verbose',
        action='store_true',
        help="Enable verbose output"
    )

    parser.add_argument(
        "-d", '--data',
        type=json_or_string,
        help="data as string or json to be send"
    )

    parser.add_argument(
        "-H", '--header',
        dest="headers",
        type=json_or_string,
        default='Content-Type: application/json',
        help="Add a custom header to the request."
    )
    
    parser.add_argument("url", help="Http url")

    args = parser.parse_args()
    
    client = HTTPClient()
    
    client.send(
        url=args.url,
        method=args.method,
        headers=args.headers,
        data=args.data,
        verbose=args.verbose
    )

if __name__ == "__main__":
    main()