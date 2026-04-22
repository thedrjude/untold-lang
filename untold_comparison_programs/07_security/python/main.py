# Security: Hashing & Encoding
import hashlib
import hmac
import base64
import secrets

password = "MySecurePassword123"

# SHA256 hashing
hash = hashlib.sha256(password.encode()).hexdigest()
print(f"SHA256: {hash}")

# SHA512 hashing
hash512 = hashlib.sha512(password.encode()).hexdigest()
print(f"SHA512: {hash512}")

# HMAC
hmac_val = hmac.new(b"secret_key", password.encode(), hashlib.sha256).hexdigest()
print(f"HMAC-SHA256: {hmac_val}")

# Base64 encoding
encoded = base64.b64encode(password.encode()).decode()
print(f"Base64: {encoded}")

# Constant-time comparison
stored_hash = hashlib.sha256(b"password").hexdigest()
if hmac.compare_digest(stored_hash, hash):
    print("Secure match!")

# Verify hash
computed = hashlib.sha256(password.encode()).hexdigest()
if hmac.compare_digest(computed, computed):
    print("Hash verified!")

# Random token generation
token = secrets.token_hex(32)
print(f"Random token: {token}")