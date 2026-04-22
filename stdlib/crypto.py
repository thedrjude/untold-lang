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
        """Constant-time comparison - prevents timing attacks"""
        return hmac.compare_digest(str(a), str(b))

    @staticmethod
    def timing_safe_compare(a, b):
        """Timing-safe string comparison for sensitive data"""
        return hmac.compare_digest(str(a), str(b))

    @staticmethod
    def verify_hash(password, hash_value, method="sha256"):
        """Verify password against hash using timing-safe comparison"""
        if method == "sha256":
            computed = hashlib.sha256(str(password).encode()).hexdigest()
        elif method == "sha512":
            computed = hashlib.sha512(str(password).encode()).hexdigest()
        else:
            computed = hashlib.blake2b(str(password).encode()).hexdigest()
        return hmac.compare_digest(computed, str(hash_value))

    @staticmethod
    def constant_time_compare(a, b):
        """Constant-time compare for cryptographic purposes"""
        a_bytes = str(a).encode()
        b_bytes = str(b).encode()
        return hmac.compare_digest(a_bytes, b_bytes)

    @staticmethod
    def pbkdf2(password, salt, iterations=100000):
        """PBKDF2 key derivation"""
        return hashlib.pbkdf2_hmac(
            'sha256', str(password).encode(), str(salt).encode(), iterations
        ).hex()