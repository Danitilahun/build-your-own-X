# Build Your Own Traceroute

A Python implementation of the `traceroute` tool that traces the network path to a destination host.

## Overview

Traceroute is a tool that discovers the route that packets take from a source computer to a destination host. It works by sending UDP packets with incrementally increasing Time-To-Live (TTL) values and listening for ICMP Time Exceeded responses.

## Features

### Step 1: Basic Header

- Accepts hostname as command-line argument
- Prints header line with destination info and hop count

### Step 2: Socket Creation & TTL

- Creates raw ICMP socket for receiving responses
- Creates UDP socket for sending probes
- Sets TTL for each probe
- Uses standard traceroute UDP port range (33434-33534)

### Step 3: Hostname Resolution

- Attempts to resolve IP addresses to hostnames
- Falls back to IP address if resolution fails
- Displays both hostname and IP in output

### Step 4: TTL Incrementation & Timeouts

- Increments TTL until destination is reached
- Handles timeouts gracefully with wildcard (\*) markers
- Sends 3 probes per hop for reliability

### Step 5: Round Trip Time (RTT)

- Records latency for each response in milliseconds
- Displays RTT in traceroute output format
- Multiple hops with different IPs are properly formatted

## Installation

```bash
# Clone the repository
cd "Build Your Own Traceroute"

# Install the package
pip install -e .
```

## Usage

```bash
# Basic usage
mytraceroute google.com

# Custom max hops
mytraceroute --max-hops 32 google.com

# Custom timeout
mytraceroute --timeout 5.0 google.com

# Combined options
mytraceroute --max-hops 32 --timeout 3.0 dns.google.com
```

## Example Output

```
traceroute to dns.google.com (8.8.4.4), 64 hops max, 32 byte packets
1  192.168.68.1 (192.168.68.1) 5.131 ms
2  broadband (192.168.1.1) 4.999 ms
3  *  * *
4  63.130.172.45 (63.130.172.45) 30.561 ms
5  195.66.236.125 (195.66.236.125) 29.541 ms
6  74.125.242.97 (74.125.242.97) 36.641 ms
7  142.251.52.151 (142.251.52.151) 32.878 ms
8  dns.google (8.8.4.4) 35.859 ms
```

## Architecture

### Core Components

#### `Traceroute` Class

- **`__init__`**: Initializes with hostname, resolves IP, sets up parameters
- **`run`**: Main entry point, orchestrates the traceroute process
- **`_trace_hop`**: Sends probes for a single TTL level, collects responses
- **`_get_hostname`**: Performs reverse DNS lookup for IP addresses
- **`_print_hop_result`**: Formats and prints hop information

### Key Implementation Details

1. **ICMP Socket**: Raw socket for receiving ICMP Time Exceeded messages
2. **UDP Socket**: Standard socket for sending probes to high-numbered UDP ports
3. **TTL Handling**: Each probe has a specific TTL value that increments with each hop
4. **Port Management**: Uses UDP ports 33434-33534 as per standard traceroute
5. **Timeout Handling**: Uses socket timeout to detect unreachable/unresponsive hosts

## Dependencies

- Python 3.6+
- icmplib >= 3.0.0

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest -v tests/

# Run specific test class
python -m pytest tests/test_traceroute.py::TestStep5 -v

# Run with coverage
python -m pytest --cov=src tests/
```

## Test Coverage

The test suite includes:

- **Unit Tests**: Individual component testing with mocks

  - Initialization tests
  - Hostname resolution tests
  - Payload creation tests
  - Output formatting tests

- **Step-specific Tests**: Tests for each implementation step

  - Step 1: Header output
  - Step 2: Socket creation and TTL
  - Step 3: Hostname resolution
  - Step 4: TTL incrementation and timeouts
  - Step 5: RTT measurement and formatting

- **Integration Tests**: End-to-end functionality tests

## Implementation Notes

### Platform Compatibility

- **Linux/macOS**: Full functionality with raw sockets
- **Windows**: May require elevated privileges for raw ICMP sockets. Consider using `icmplib` on Windows for better compatibility.

### Performance Considerations

- Default timeout: 2 seconds per hop
- Default max hops: 64 (industry standard)
- Each hop sends 3 probes for reliability
- Unique IPs are aggregated in output

### Error Handling

- Invalid hostnames are caught and reported
- Failed DNS lookups fall back to IP addresses
- Socket errors are handled gracefully
- Timeout errors show as wildcard markers

## References

- [Man page: traceroute](https://linux.die.net/man/8/traceroute)
- [RFC 792: ICMP](https://tools.ietf.org/html/rfc792)
- [UDP Protocol](https://tools.ietf.org/html/rfc768)

## Author

Built as part of the Coding Challenges series.
