import pytest
import json
from stdlib.web import UntoldWeb as web

class TestWeb:
    def test_get_success(self):
        res = web.get("https://httpbin.org/get")
        assert res["status"] == 200
        assert res["ok"] == True
        assert "body" in res
    
    def test_get_404(self):
        res = web.get("https://httpbin.org/status/404")
        assert res["status"] == 404
        assert res["ok"] == False
    
    def test_get_json(self):
        res = web.get_json("https://httpbin.org/json")
        assert res["status"] == 200
        assert res["json"] is not None
    
    def test_post(self):
        res = web.post("https://httpbin.org/post", {"test": "data"})
        assert res["status"] == 200
        assert res["ok"] == True
    
    def test_url_encode(self):
        assert web.url_encode("hello world") == "hello%20world"
        assert web.url_encode("a=b&c=d") == "a%3Db%26c%3Dd"
    
    def test_url_decode(self):
        assert web.url_decode("hello%20world") == "hello world"
    
    def test_parse_json(self):
        data = '{"key": "value", "num": 42}'
        obj = web.parse_json(data)
        assert obj["key"] == "value"
        assert obj["num"] == 42
    
    def test_to_json(self):
        obj = {"name": "test", "value": 123}
        json_str = web.to_json(obj)
        assert "test" in json_str
        assert "123" in json_str