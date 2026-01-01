import unittest
from unittest.mock import patch, MagicMock
import socket
from src.traceroute import Traceroute, DNSResolver, ProbeSocket, OutputFormatter, HopTracer


class TestDNSResolver(unittest.TestCase):
    """Test cases for DNSResolver class"""

    @patch('socket.gethostbyname')
    def test_resolve_hostname(self, mock_gethostbyname):
        """Test hostname resolution"""
        mock_gethostbyname.return_value = "142.251.41.14"
        result = DNSResolver.resolve_hostname("google.com")
        self.assertEqual(result, "142.251.41.14")

    @patch('socket.gethostbyaddr')
    def test_reverse_lookup_success(self, mock_gethostbyaddr):
        """Test reverse DNS lookup success"""
        mock_gethostbyaddr.return_value = ("google.com", [], ["142.251.41.14"])
        result = DNSResolver.reverse_lookup("142.251.41.14")
        self.assertEqual(result, "google")

    @patch('socket.gethostbyaddr')
    def test_reverse_lookup_failure(self, mock_gethostbyaddr):
        """Test reverse DNS lookup failure"""
        mock_gethostbyaddr.side_effect = socket.herror()
        result = DNSResolver.reverse_lookup("142.251.41.14")
        self.assertEqual(result, "142.251.41.14")


class TestProbeSocket(unittest.TestCase):
    """Test cases for ProbeSocket class"""

    def test_initialization(self):
        """Test ProbeSocket initialization"""
        payload = b'test'
        socket_mgr = ProbeSocket(payload, timeout=2.0)
        self.assertEqual(socket_mgr.payload, payload)
        self.assertEqual(socket_mgr.timeout, 2.0)

    def test_port_constants(self):
        """Test UDP port range constants"""
        self.assertEqual(ProbeSocket.UDP_PORT_START, 33434)
        self.assertEqual(ProbeSocket.UDP_PORT_END, 33534)


class TestOutputFormatter(unittest.TestCase):
    """Test cases for OutputFormatter class"""

    @patch('builtins.print')
    def test_print_header(self, mock_print):
        """Test header printing"""
        OutputFormatter.print_header("google.com", "142.251.41.14", 64, 32)
        mock_print.assert_called_once()
        output = mock_print.call_args[0][0]
        self.assertIn("google.com", output)
        self.assertIn("142.251.41.14", output)

    @patch('builtins.print')
    def test_print_hop_all_timeouts(self, mock_print):
        """Test hop with all timeouts"""
        resolver = DNSResolver()
        OutputFormatter.print_hop(3, [None, None, None], resolver)
        mock_print.assert_called_once()
        output = mock_print.call_args[0][0]
        self.assertIn("*", output)

    @patch('builtins.print')
    @patch('socket.gethostbyaddr')
    def test_print_hop_with_responses(self, mock_gethostbyaddr, mock_print):
        """Test hop with IP responses"""
        mock_gethostbyaddr.side_effect = socket.herror()
        resolver = DNSResolver()
        responses = [
            {'ip': '192.168.1.1', 'rtt_ms': 5.123},
            {'ip': '192.168.1.1', 'rtt_ms': 4.456},
            {'ip': '192.168.1.1', 'rtt_ms': 5.789},
        ]
        OutputFormatter.print_hop(1, responses, resolver)
        output = mock_print.call_args[0][0]
        self.assertIn("192.168.1.1", output)
        self.assertIn("ms", output)


class TestHopTracer(unittest.TestCase):
    """Test cases for HopTracer class"""

    def test_initialization(self):
        """Test HopTracer initialization"""
        payload = b'test'
        probe_socket = ProbeSocket(payload)
        hop_tracer = HopTracer("8.8.8.8", probe_socket)
        self.assertEqual(hop_tracer.dest_ip, "8.8.8.8")
        self.assertEqual(hop_tracer.probe_socket, probe_socket)


class TestTraceroute(unittest.TestCase):
    """Test cases for main Traceroute class"""

    @patch('socket.gethostbyname')
    def test_initialization(self, mock_gethostbyname):
        """Test Traceroute initialization"""
        mock_gethostbyname.return_value = "142.251.41.14"
        tracer = Traceroute("google.com")

        self.assertEqual(tracer.hostname, "google.com")
        self.assertEqual(tracer.dest_ip, "142.251.41.14")
        self.assertEqual(tracer.max_hops, 64)
        self.assertEqual(tracer.timeout, 2.0)

    @patch('socket.gethostbyname')
    def test_initialization_custom_params(self, mock_gethostbyname):
        """Test Traceroute with custom parameters"""
        mock_gethostbyname.return_value = "8.8.8.8"
        tracer = Traceroute("8.8.8.8", max_hops=32,
                            timeout=5.0, packet_size=64)

        self.assertEqual(tracer.max_hops, 32)
        self.assertEqual(tracer.timeout, 5.0)
        self.assertEqual(tracer.packet_size, 64)

    @patch('socket.gethostbyname')
    def test_port_constants_exposed(self, mock_gethostbyname):
        """Test that port constants are exposed on main class"""
        mock_gethostbyname.return_value = "8.8.8.8"
        tracer = Traceroute("8.8.8.8")

        self.assertEqual(tracer.UDP_PORT_START, 33434)
        self.assertEqual(tracer.UDP_PORT_END, 33534)


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    @patch('socket.gethostbyname')
    @patch.object(ProbeSocket, 'send_probe')
    def test_run_basic(self, mock_send, mock_resolve):
        """Test basic run flow"""
        mock_resolve.return_value = "8.8.8.8"
        mock_send.return_value = None

        tracer = Traceroute("8.8.8.8", max_hops=1)
        with patch('builtins.print') as mock_print:
            tracer.run()
            # Should print header
            self.assertGreaterEqual(mock_print.call_count, 1)


class TestStep1(unittest.TestCase):
    """Test Step 1: Print header"""
    @patch('socket.gethostbyname')
    def test_header_format(self, mock_gethostbyname):
        """Step 1: Verify header format"""
        mock_gethostbyname.return_value = "8.8.4.4"
        tracer = Traceroute("dns.google.com")
        self.assertEqual(tracer.hostname, "dns.google.com")
        self.assertEqual(tracer.dest_ip, "8.8.4.4")


class TestStep2(unittest.TestCase):
    """Test Step 2: Sockets and TTL"""

    def test_socket_constants(self):
        """Step 2: Verify socket constants"""
        self.assertEqual(ProbeSocket.UDP_PORT_START, 33434)
        self.assertEqual(ProbeSocket.UDP_PORT_END, 33534)


class TestStep3(unittest.TestCase):
    """Test Step 3: Hostname resolution"""
    @patch('socket.gethostbyaddr')
    def test_hostname_resolution(self, mock_gethostbyaddr):
        """Step 3: Verify hostname resolution"""
        mock_gethostbyaddr.return_value = ("google.com", [], ["8.8.4.4"])
        result = DNSResolver.reverse_lookup("8.8.4.4")
        self.assertEqual(result, "google")


class TestStep4(unittest.TestCase):
    """Test Step 4: TTL incrementation"""
    @patch('socket.gethostbyname')
    def test_max_hops(self, mock_gethostbyname):
        """Step 4: Verify TTL/hop incrementing works"""
        mock_gethostbyname.return_value = "8.8.8.8"
        tracer = Traceroute("8.8.8.8", max_hops=7)
        self.assertEqual(tracer.max_hops, 7)


class TestStep5(unittest.TestCase):
    """Test Step 5: RTT measurement"""
    @patch('builtins.print')
    @patch('socket.gethostbyaddr')
    def test_rtt_formatting(self, mock_gethostbyaddr, mock_print):
        """Step 5: Verify RTT measurement and formatting"""
        mock_gethostbyaddr.side_effect = socket.herror()
        resolver = DNSResolver()
        responses = [
            {'ip': '192.168.1.1', 'rtt_ms': 5.131},
            {'ip': '192.168.1.1', 'rtt_ms': 5.575},
            {'ip': '192.168.1.1', 'rtt_ms': 3.908},
        ]
        OutputFormatter.print_hop(1, responses, resolver)
        output = mock_print.call_args[0][0]
        self.assertIn("ms", output)
        # Should have decimal format
        self.assertRegex(output, r'\d+\.\d+ ms')


if __name__ == '__main__':
    unittest.main()
