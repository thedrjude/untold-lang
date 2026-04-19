import pytest
import socket
from stdlib.net import UntoldNet as net

class TestNet:
    def test_port_open(self):
        result = net.port_open("google.com", 443)
        assert result == True
    
    def test_port_closed(self):
        result = net.port_open("google.com", 9999)
        assert result == False
    
    def test_resolve(self):
        result = net.resolve("google.com")
        assert result is not None
        assert "." in result
    
    def test_my_ip(self):
        result = net.my_ip()
        assert result is not None
        assert len(result) > 0