import socket
import json
from urllib.parse import urlparse

class HTTPClient:
    def __init__(self):
        pass

    def send(self, url, method="GET", headers=None, data=None, verbose=False):
        parsed_url = urlparse(url)
        
        # Step 1
        host = parsed_url.hostname
        port = parsed_url.port if parsed_url.port else (
            80 if parsed_url.scheme == 'http' else 443)
        path = parsed_url.path if parsed_url.path else "/"

        # Step 2
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            host_ip = socket.gethostbyname(host)
            if verbose:
                print(host_ip)
                print(f"Protocol : {parsed_url.scheme}")
                print(f"Host : {host}")
                print(f"Port : {port}")
                print(f"Path : {path}")

            client.connect((host_ip, port))
            print(f"Successfully connected to {host} on port {port}.\n")
        except Exception as e:
            print(f"Error: {e}")
            return

        request = f"{method} {path} HTTP/1.1\r\n"
        request += f"Host: {host}\r\n"
        request += "Accept: */*\r\n"
        request += "Connection: close\r\n"
        
        body = None
        
        if method in ["POST", "PUT", "PATCH"]:
            if data:
                if isinstance(data, dict):
                    body = json.dumps(data)
                else:
                    body = data
            
                body_bytes = body.encode("utf-8")
                content_length = len(body_bytes)
                
                if headers:
                    request += f"{headers}\r\n"
                
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
            response_bytes += chunk
            
        client.close()

        response = response_bytes.decode('utf-8', errors='ignore')
        response_header, response_body = response.split('\r\n\r\n', 1)

        # Step 3
        if verbose:
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