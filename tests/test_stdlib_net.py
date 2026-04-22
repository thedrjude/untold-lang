from stdlib.net import UntoldNet


class TestNet:
    def test_port_open(self):
        result = UntoldNet.port_open("google.com", 443)
        assert result is True
    
    def test_port_closed(self):
        result = UntoldNet.port_open("google.com", 9999)
        assert result is False
    
    def test_resolve(self):
        result = UntoldNet.resolve("google.com")
        assert result is not None
        assert "." in result
    
    def test_my_ip(self):
        result = UntoldNet.my_ip()
        assert result is not None
        assert len(result) > 0