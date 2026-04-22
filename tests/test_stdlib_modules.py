from stdlib.ai import UntoldAI
from stdlib.hack import UntoldHack
from stdlib.shell import UntoldShell


class TestAI:
    def test_sentiment_positive(self):
        result = UntoldAI.sentiment("This is amazing! I love it so much!")
        assert result["label"] == "positive"
        assert result["score"] > 0
    
    def test_sentiment_negative(self):
        result = UntoldAI.sentiment("This is terrible and awful. I hate it!")
        assert result["label"] == "negative"
    
    def test_sentiment_neutral(self):
        result = UntoldAI.sentiment("This is a test.")
        assert result["label"] == "neutral"
    
    def test_keywords(self):
        text = "Python is a great programming language for AI and machine learning"
        keywords = UntoldAI.keywords(text, 3)
        assert len(keywords) <= 3
        assert isinstance(keywords, list)
    
    def test_summarize(self):
        text = "This is sentence one. This is sentence two. This is sentence three."
        summary = UntoldAI.summarize(text, 1)
        assert isinstance(summary, str)
    
    def test_dot(self):
        a = [1, 2, 3]
        b = [4, 5, 6]
        result = UntoldAI.dot(a, b)
        assert result == 32  # 1*4 + 2*5 + 3*6
    
    def test_normalize(self):
        vector = [3, 4]
        result = UntoldAI.normalize(vector)
        assert abs(result[0]**2 + result[1]**2 - 1) < 0.001


class TestHack:
    def test_sha256(self):
        result = UntoldHack.sha256("hello")
        assert result == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    
    def test_md5(self):
        result = UntoldHack.md5("hello")
        assert result == "5d41402abc4b2a76b9719d911017c592"
    
    def test_b64_encode(self):
        result = UntoldHack.b64_encode("hello")
        assert result == "aGVsbG8="
    
    def test_b64_decode(self):
        result = UntoldHack.b64_decode("aGVsbG8=")
        assert result == "hello"
    
    def test_hex_encode(self):
        result = UntoldHack.hex_encode("hello")
        assert result == "68656c6c6f"
    
    def test_hex_decode(self):
        result = UntoldHack.hex_decode("68656c6c6f")
        assert result == "hello"
    
    def test_url_encode(self):
        result = UntoldHack.url_encode("hello world")
        assert result == "hello%20world"
    
    def test_url_decode(self):
        result = UntoldHack.url_decode("hello%20world")
        assert result == "hello world"
    
    def test_random_bytes(self):
        result = UntoldHack.random_bytes(16)
        assert len(result) == 32  # hex encoded
        assert all(c in "0123456789abcdef" for c in result)


class TestShell:
    def test_platform(self):
        result = UntoldShell.platform()
        assert result in ["linux", "Linux", "windows", "Windows", "darwin", "Darwin"]
    
    def test_args(self):
        result = UntoldShell.args()
        assert isinstance(result, list)
    
    def test_env_get(self):
        result = UntoldShell.env("PATH")
        assert result is not None or result == ""