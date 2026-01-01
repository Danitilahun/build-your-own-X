from src.client import HTTPClient

BASE_URL = "http://eu.httpbin.org"

class TestHTTPClient:
    
    def setup_method(self):
        """Runs before every test"""
        self.client = HTTPClient()

    def test_simple_get_request(self, capsys):
        """
        Test a basic GET request.
        capsys: A pytest fixture that captures print() output.
        """
        url = f"{BASE_URL}/get"
        
        # 1. Run the code
        self.client.send(url, method="GET")
        
        # 2. Capture what was printed to stdout/stderr
        captured = capsys.readouterr()
        
        # 3. Assertions
        # Check if the output contains valid JSON from httpbin
        assert '"url": "http://eu.httpbin.org/get"' in captured.out
        # Ensure we didn't print verbose logs to stdout (standard output)
        assert "Connecting to" not in captured.out

    def test_post_request_with_data(self, capsys):
        """Test sending JSON data via POST"""
        url = f"{BASE_URL}/post"
        data = {"username": "admin", "id": 123}
        
        self.client.send(url, method="POST", data=data)
        
        captured = capsys.readouterr()
        
        # Httpbin returns the data we sent in the "json" field
        assert '"username": "admin"' in captured.out
        assert '"id": 123' in captured.out

    def test_custom_headers(self, capsys):
        """Test sending a custom header"""
        url = f"{BASE_URL}/headers"
        headers = "X-My-Custom-Header: PyCurlTest"
        
        self.client.send(url, method="GET", headers=headers)
        
        captured = capsys.readouterr()
        
        # Check if server received our custom header
        assert '"X-My-Custom-Header": "PyCurlTest"' in captured.out

    def test_verbose_mode(self, capsys):
        """Test that verbose mode prints protocol info to stderr (or stdout depending on your impl)"""
        url = f"{BASE_URL}/get"
        
        # Enable verbose
        self.client.send(url, method="GET", verbose=True)
        
        captured = capsys.readouterr()
        
        # If you used logging (stderr), check captured.err
        # If you used print (stdout) for verbose, check captured.out
        
        # Assuming you used print for verbose in step 3:
        assert "> GET /get HTTP/1.1" in captured.out
        assert "< Content-Type: application/json" in captured.out