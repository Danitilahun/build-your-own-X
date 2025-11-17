import argparse
from urllib.parse import urlparse
import socket
import json


# Step 1

parser = argparse.ArgumentParser(
    description="A simple tool to learn how to command line tool.")

def json_or_string(value):
    
    try:
        return json.loads(value)
    
    except json.JSONDecodeError:
        return value

parser.add_argument(
    "-X",
    "--request",
    dest="method",
    default="GET",
    choices=["GET", "POST", "PUT","DELETE", "HEAD","PATCH"],
    help="Specify a custom request method to use (e.g., GET, POST, DELETE)."
)

parser.add_argument(
    "-v",
    '--verbose',
    action='store_true',
    help="Enable verbose output"
)

parser.add_argument(
    "-d",
    '--data',
    type=json_or_string,
    # required=True,
    help="data as string or json to be send"
)

def key_value_pair(value):
    try:
        key, val = value.split(':', 1)
        return (key.strip(), val.strip())
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid Key:Value header.")

parser.add_argument(
    "-H",
    '--header',
    dest="headers",
    type=json_or_string,
    # action="append",
    default='Content-Type: application/json',
    help="Add a custom header to the request."
)
parser.add_argument("url", help="Http url")

args = parser.parse_args()
print(args)
print("URL", args.url)

parsed_url = urlparse(args.url)

print("Protocol :", parsed_url.scheme)
print("Host :", parsed_url.hostname)
print("Port :", parsed_url.port if parsed_url.port else (
    80 if parsed_url.scheme == 'http' else 443))
print("Path :", parsed_url.path)


host = parsed_url.hostname
port = parsed_url.port if parsed_url.port else (
    80 if parsed_url.scheme == 'http' else 443)
path = parsed_url.path

# Step 2

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    host_ip = socket.gethostbyname(parsed_url.hostname)
    print(host_ip)

    client.connect((host_ip, port))
    print(f"Successfully connected to {host} on port {port}.\n")
except Exception as e:
    print(f"Error: {e}")
    
request = f"{args.method} {path} HTTP/1.1\r\n"
request += f"Host: {host}\r\n"
request += "Accept: */*\r\n"
request += "Connection: close\r\n"
   
body = None
 
if args.method in ["POST", "PUT", "PATCH"]:
    if args.data:
        if isinstance(args.data,dict):
            body = json.dumps(args.data)
        else:
            body = args.data
    
        body_bytes = body.encode("utf-8")
        content_length = len(body_bytes)
        
        request += f"{args.headers}\r\n"
        request += f"Content-Length: {content_length}\r\n"
    
request += "Connection: close\r\n"
request += "\r\n"

if body:
    request += body
    
print("Sending request", request)

client.sendall(request.encode())

print("Request sent.\n")

response_bytes = b""
while True:
    chunk = client.recv(4096)
    if not chunk:
        break
    
    response_bytes+=chunk
    
client.close()

response = response_bytes.decode('utf-8', errors='ignore')

response_header, response_body = response.split('\r\n\r\n',1)
# print(response_body)

# Step 3
if args.verbose:
    raw_request = request.splitlines()
    request_verbose_mode = [f'> {line}' for line in raw_request]
    request_verbose_mode = "\n".join(request_verbose_mode)
    print(request_verbose_mode)
    
    raw_response = response_header.splitlines()
    response_verbose_mode = [f'< {line}' for line in raw_response]
    response_verbose_mode = "\n".join(response_verbose_mode)
    print(response_verbose_mode)
    print(response_body)
else:
    print(response_body)
