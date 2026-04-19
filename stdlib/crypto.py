"""
untold.crypto — Cryptography module
"""
import hashlib
import hmac
import secrets


class UntoldCrypto:
    """Cryptographic utilities"""

    @staticmethod
    def sha256(data):
        """Hash data with SHA-256"""
        return hashlib.sha256(str(data).encode()).hexdigest()

    @staticmethod
    def sha512(data):
        """Hash data with SHA-512"""
        return hashlib.sha512(str(data).encode()).hexdigest()

    @staticmethod
    def blake2b(data):
        """Hash data with BLAKE2b"""
        return hashlib.blake2b(str(data).encode()).hexdigest()

    @staticmethod
    def hmac_sha256(key, message):
        """Create HMAC-SHA256"""
        return hmac.new(str(key).encode(), str(message).encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def hmac_sha512(key, message):
        """Create HMAC-SHA512"""
        return hmac.new(str(key).encode(), str(message).encode(), hashlib.sha512).hexdigest()

    @staticmethod
    def random_token(length=32):
        """Generate random token"""
        return secrets.token_hex(length)

    @staticmethod
    def random_bytes(length=32):
        """Generate random bytes"""
        return secrets.token_bytes(length)

    @staticmethod
    def secure_compare(a, b):
        """Constant-time comparison"""
        return hmac.compare_digest(str(a), str(b))

    @staticmethod
    def pbkdf2(password, salt, iterations=100000):
        """PBKDF2 key derivation"""
        return hashlib.pbkdf2_hmac(
            'sha256', str(password).encode(), str(salt).encode(), iterations
        ).hex()