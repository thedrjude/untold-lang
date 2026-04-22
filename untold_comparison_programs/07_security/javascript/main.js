// Security: Hashing & Encoding
const crypto = require('crypto');

const password = "MySecurePassword123";

// SHA256 hashing
const hash = crypto.createHash('sha256').update(password).digest('hex');
console.log(`SHA256: ${hash}`);

// SHA512 hashing
const hash512 = crypto.createHash('sha512').update(password).digest('hex');
console.log(`SHA512: ${hash512}`);

// HMAC
const hmacVal = crypto.createHmac('sha256', 'secret_key').update(password).digest('hex');
console.log(`HMAC-SHA256: ${hmacVal}`);

// Base64 encoding
const encoded = Buffer.from(password).toString('base64');
console.log(`Base64: ${encoded}`);

// Constant-time comparison
const storedHash = crypto.createHash('sha256').update('password').digest('hex');
if (crypto.timingSafeEqual(Buffer.from(storedHash), Buffer.from(hash))) {
    console.log("Secure match!");
}

// Verify hash
const computed = crypto.createHash('sha256').update(password).digest('hex');
if (hash === computed) {
    console.log("Hash verified!");
}

// Random token generation
const token = crypto.randomBytes(32).toString('hex');
console.log(`Random token: ${token}`);