from stdlib.web import UntoldWeb


class TestWeb:
    def test_get_success(self):
        res = UntoldWeb.get("https://httpbin.org/get")
        assert res["status"] == 200
        assert res["ok"] is True
        assert "body" in res
    
    def test_get_404(self):
        res = UntoldWeb.get("https://httpbin.org/status/404")
        assert res["status"] == 404
        assert not res["ok"]
    
    def test_get_json(self):
        res = UntoldWeb.get_json("https://httpbin.org/json")
        assert res["status"] == 200
        assert res["json"] is not None
    
    def test_post(self):
        res = UntoldWeb.post("https://httpbin.org/post", {"test": "data"})
        assert res["status"] == 200
        assert res["ok"] is True
    
    def test_url_encode(self):
        assert UntoldWeb.url_encode("hello world") == "hello%20world"
        assert UntoldWeb.url_encode("a=b&c=d") == "a%3Db%26c%3Dd"
    
    def test_url_decode(self):
        assert UntoldWeb.url_decode("hello%20world") == "hello world"
    
    def test_parse_json(self):
        data = '{"key": "value", "num": 42}'
        obj = UntoldWeb.parse_json(data)
        assert obj["key"] == "value"
        assert obj["num"] == 42
    
    def test_to_json(self):
        obj = {"name": "test", "value": 123}
        json_str = UntoldWeb.to_json(obj)
        assert "test" in json_str
        assert "123" in json_str