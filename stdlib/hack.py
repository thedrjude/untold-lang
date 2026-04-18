import socket
import subprocess
import hashlib
import base64
import os
import re
import urllib.request

class UntoldHack:
    """
    untold.hack — Security & ethical hacking tools module.
    For educational and authorized use only.
    """

    # ── Hashing ───────────────────────────────────────────────
    @staticmethod
    def md5(text):
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def sha1(text):
        return hashlib.sha1(text.encode()).hexdigest()

    @staticmethod
    def sha256(text):
        return hashlib.sha256(text.encode()).hexdigest()

    @staticmethod
    def sha512(text):
        return hashlib.sha512(text.encode()).hexdigest()

    # ── Encoding ──────────────────────────────────────────────
    @staticmethod
    def b64_encode(text):
        return base64.b64encode(text.encode()).decode()

    @staticmethod
    def b64_decode(text):
        return base64.b64decode(text.encode()).decode(errors="replace")

    @staticmethod
    def hex_encode(text):
        return text.encode().hex()

    @staticmethod
    def hex_decode(text):
        return bytes.fromhex(text).decode(errors="replace")

    @staticmethod
    def url_encode(text):
        import urllib.parse
        return urllib.parse.quote(text)

    @staticmethod
    def url_decode(text):
        import urllib.parse
        return urllib.parse.unquote(text)

    # ── Network recon ─────────────────────────────────────────
    @staticmethod
    def resolve(host):
        try:
            return socket.gethostbyname(host)
        except:
            return None

    @staticmethod
    def reverse_dns(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None

    @staticmethod
    def port_scan(host, start, end, timeout=0.5):
        """Scan ports on a host. Authorized use only."""
        open_ports = []
        for port in range(int(start), int(end) + 1):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(timeout)
                if s.connect_ex((host, port)) == 0:
                    open_ports.append(port)
                s.close()
            except:
                pass
        return open_ports

    @staticmethod
    def banner_grab(host, port, timeout=3):
        """Grab service banner from open port."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((host, int(port)))
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode(errors="replace")
            s.close()
            return banner.strip()
        except Exception as e:
            return str(e)

    @staticmethod
    def whois(domain):
        """Basic whois via shell."""
        result = subprocess.run(
            ["whois", domain],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout[:2000]

    # ── Web security ──────────────────────────────────────────
    @staticmethod
    def headers(url):
        """Fetch HTTP headers from a URL."""
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "UntoldLang-Security/0.1")
            with urllib.request.urlopen(req, timeout=10) as r:
                return dict(r.headers)
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def find_emails(text):
        return re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)

    @staticmethod
    def find_urls(text):
        return re.findall(r"https?://[^\s\"'>]+", text)

    @staticmethod
    def find_ips(text):
        return re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)

    # ── Crypto helpers ────────────────────────────────────────
    @staticmethod
    def random_bytes(n=16):
        return os.urandom(int(n)).hex()

    @staticmethod
    def xor_cipher(text, key):
        """Simple XOR cipher — for educational purposes."""
        key   = (key * (len(text) // len(key) + 1))[:len(text)]
        xored = bytes(a ^ b for a, b in zip(text.encode(), key.encode()))
        return xored.hex()

    @staticmethod
    def caesar_cipher(text, shift):
        """Caesar cipher — shift letters by n positions."""
        result = []
        for ch in text:
            if ch.isalpha():
                base = ord("A") if ch.isupper() else ord("a")
                result.append(chr((ord(ch) - base + int(shift)) % 26 + base))
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def wordlist_gen(base, numbers=True, specials=False):
        """Generate a simple wordlist from a base word."""
        words = [base, base.upper(), base.capitalize()]
        if numbers:
            for n in ["1", "12", "123", "1234", "2024", "2025", "!"]:
                words.append(base + n)
                words.append(base.capitalize() + n)
        if specials:
            for s in ["!", "@", "#", "_"]:
                words.append(base + s)
        return words