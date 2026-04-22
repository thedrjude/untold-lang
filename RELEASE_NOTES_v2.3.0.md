# Untold Lang v2.1.1 — Security & Performance Update

**Release Date:** April 2026  
**Author:** Antony Jude  
**License:** MIT

---

## What's New in v2.1.1

This release focuses on **security improvements** and **performance enhancements** based on community feedback and comparison analysis.

---

## 1. Native Compilation (C Backend) 🚀

### Performance Boost: 10x Faster

We've added a native C code generator for maximum performance.

```bash
# Compile Untold to C
untold compile-c main.ut

# Compile and run native binary
gcc -O2 -o program main.c -lm
./program
```

**Features:**
- Generate clean C code from Untold source
- Optimized memory management
- Built-in hashing functions
- Constant-time comparison support

---

## 2. Enhanced Security 🔒

### Constant-Time Comparison

Prevents timing attacks on sensitive data.

```untold
use untold.crypto

let hash1 = crypto.sha256("password123")
let hash2 = crypto.sha256("password456")

// Timing-safe comparison (prevents timing attacks)
if crypto.secure_compare(hash1, hash2) {
    say("Match!")
} else {
    say("No match")
}

// Verify password against hash securely
if crypto.verify_hash("mypassword", stored_hash, "sha256") {
    say("Access granted")
}
```

### New Security Functions

| Function | Description |
|----------|-------------|
| `crypto.secure_compare(a, b)` | Constant-time string comparison |
| `crypto.timing_safe_compare(a, b)` | Timing-safe for crypto operations |
| `crypto.verify_hash(pwd, hash, method)` | Secure password verification |
| `crypto.constant_time_compare(a, b)` | Cryptographic constant-time compare |
| `hack.secure_compare(a, b)` | Same in hack module |
| `hack.timing_safe_compare(a, b)` | Same in hack module |
| `hack.verify_hash(pwd, hash, method)` | Same in hack module |

---

## 3. Improved Async Patterns ⚡

Enhanced async/await for better concurrency.

```untold
// Run multiple async operations in parallel
let results = await_all([
    http.get("https://api1.example.com"),
    http.get("https://api2.example.com"),
    http.get("https://api3.example.com")
])

// Run functions in parallel
parallel(fn1, fn2, fn3)

// Create async wrapper
let myAsync = async_fn(myFunction)
```

### New Async Builtins

| Function | Description |
|----------|-------------|
| `async_fn(fn)` | Create async function wrapper |
| `await_all(promises)` | Await multiple promises concurrently |
| `parallel(*fns)` | Run functions in parallel |
| `wait` (enhanced) | Better async handling |

---

## 4. Expanded Package Ecosystem 📦

20+ new packages added to the registry!

### Categories

**Utilities:**
- `colors` — Colorful terminal output
- `uuid` — Generate unique identifiers
- `dotenv` — Environment variables
- `validator` — Data validation
- `logger` — Advanced logging

**Data Processing:**
- `date` — Date/time handling
- `math` — Extended math operations
- `csv` — CSV parsing/generation
- `yaml` — YAML support

**Security:**
- `jsonwebtoken` — JWT tokens
- `bcrypt` — Password hashing

**Web & Networking:**
- `websocket` — WebSocket client/server
- `graphql` — GraphQL client
- `email` — Email sending

**Database:**
- `redis` — Redis client
- `mongo` — MongoDB client

**Graphics & Documents:**
- `canvas` — 2D graphics
- `pdf` — PDF generation
- `compression` — Zip/gzip/tar

**Development:**
- `cli` — CLI application builder

---

## Benchmark Results

### Fibonacci (Recursive) — Lower is Better

| Version | Time (ms) |
|---------|-----------|
| v2.0.0 | 5.2 |
| v2.1.1 (interpreted) | 5.0 |
| v2.1.1 (native C) | 0.4 |

### Security Operations

| Operation | Status |
|-----------|--------|
| SHA256 hashing | ✅ |
| HMAC-SHA256 | ✅ |
| Constant-time compare | ✅ NEW |
| PBKDF2 | ✅ |
| Secure random | ✅ |

---

## Migration from v2.0.0

**No breaking changes!** v2.1.1 is fully backward compatible.

### New Features (Optional)

These are additive — existing code works without changes:

```untold
// Old code (still works)
use untold.hack
say(hack.sha256("test"))

// New code (enhanced)
use untold.crypto
if crypto.secure_compare(a, b) { say("secure!") }
```

---

## Bug Fixes

- Fixed async/await handling for concurrent operations
- Improved error messages for module imports
- Fixed list/map literal parsing
- Enhanced debugger performance

---

## Coming in v2.2.0

- **LSP** — Language Server Protocol for IDE support
- **Pattern matching** — Rust-style match expressions
- **WASM target** — Compile to WebAssembly

---

## Contributors

Special thanks to the community for the security feedback and performance suggestions!

---

## Links

- **Website:** https://untold-lang.github.io
- **Docs:** https://thedrjude.github.io/untold-lang/docs.html
- **GitHub:** https://github.com/untold-lang/untold
- **PyPI:** https://pypi.org/project/untold-lang/

---

*Untold Lang — The Language Without Limits*