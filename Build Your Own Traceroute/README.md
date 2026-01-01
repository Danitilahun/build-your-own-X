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

## Author

Built as part of the Coding Challenges series.
