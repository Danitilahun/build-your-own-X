import argparse
from urllib.parse import urlparse
import socket


# Step 1

parser = argparse.ArgumentParser(
    description="A simple tool to learn how to command line tool.")

parser.add_argument("url", help="Http url")

args = parser.parse_args()

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

request = f"GET {path} HTTP/1.1\r\n"
request += f"Host: {host}\r\n"
request += "Accept: */*\r\n"
request += "Connection: close\r\n"
request += "\r\n"

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
    
print(response)