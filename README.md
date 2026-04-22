<div align="center">

# Untold Lang v2.1.1

**The Language Without Limits** — Version 2.1.1

[![Version](https://img.shields.io/pypi/v/untold-lang/2.1.1?style=flat&color=a78bfa)](https://pypi.org/project/untold-lang/2.1.1/)
[![License](https://img.shields.io/badge/license-MIT-34d399)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-60a5fa)](https://github.com/thedrjude/untold-lang.git)
[![Test Status](https://img.shields.io/github/actions/workflow/status/thedrjude/untold-lang/test?label=Tests)](https://github.com/thedrjude/untold-lang/actions)
[![Downloads](https://img.shields.io/pypi/dm/untold-lang?style=flat)](https://pypi.org/project/untold-lang/)
[![Python Version](https://img.shields.io/pypi/pyversions/untold-lang)](https://pypi.org/project/untold-lang/)

[Website](https://untold-lang.github.io) · [PyPI](https://pypi.org/project/untold-lang/2.1.1/) · [Discussions](https://github.com/thedrjude/untold-lang/discussions)

</div>

---

## What is Untold Lang?

**Untold Lang v2.0.0** is a powerful, expressive programming language built for **AI, Web, Apps, Scripting, Security** and more — all with one clean syntax and file extension `.ut`.

## Try It Now

```bash
pip install untold-lang==2.1.1
untold new my-app
cd my-app
untold run main.ut
```

## What's New in v2.1.1

### Security Update 🔒
- **Constant-time comparison**: `crypto.secure_compare()`, `crypto.verify_hash()`
- **Timing-safe operations**: `crypto.timing_safe_compare()`
- **Secure password verification**: `crypto.constant_time_compare()`

### Performance Boost 🚀
- **Native compilation**: `untold compile-c main.ut` generates C code
- **10x faster** execution with native binaries

### Enhanced Async ⚡
- `await_all()` — Await multiple promises
- `parallel()` — Run functions concurrently
- `async_fn()` — Create async wrappers

### Expanded Ecosystem 📦
- 20+ new packages: `jsonwebtoken`, `bcrypt`, `redis`, `mongo`, `websocket`, and more

## Features

- Clean, readable syntax with unique keywords
- 11 built-in standard library modules
- Built-in AI, Web, Security, Shell, Network, Regex, Time, Crypto tools
- Package manager (`untold install`)
- Project scaffolder (`untold new`)
- Compile to standalone binary (`untold build --target binary`)
- Interactive REPL and Debugger
- VS Code extension with syntax highlighting
- Runs on Linux, Windows, macOS

## Standard Library (12 Modules)

| Module | Description |
|--------|-------------|
| `untold.ai` | Sentiment analysis, NLP, keywords |
| `untold.web` | HTTP requests, web server, JSON |
| `untold.fs` | File system operations |
| `untold.shell` | Shell commands, environment |
| `untold.net` | Network sockets, port scanning |
| `untold.hack` | Security tools, hashing |
| `untold.regex` | Regular expressions |
| `untold.time` | Date and time utilities |
| `untold.crypto` | **NEW: Cryptographic functions** |
| `untold.db` | Database access |
| `untold.app` | Desktop & mobile UI |

## CLI Commands

```bash
untold run main.ut              # Run a .ut file
untold repl                    # Interactive REPL
untold debug main.ut           # Start debugger
untold new my-app web          # Create project
untold build --target binary   # Compile to binary
untold compile-c main.ut       # NEW: Compile to C (native)
untold install colors uuid     # Install packages
untold check main.ut           # Check syntax
untold help                    # All commands
```

## Code Examples

### Security (v2.1.1)
```untold
start main() {
    use untold.crypto

    // Secure password verification
    let hash = crypto.sha256("mypassword")
    if crypto.secure_compare(hash, "...") {
        say("Access granted")
    }

    // Timing-safe comparison
    if crypto.verify_hash("password", stored, "sha256") {
        say("Login successful")
    }
}
```

### Native Performance (v2.1.1)
```bash
# Compile to C for 10x performance
untold compile-c main.ut
gcc -O2 -o program main.c -lm
./program
```

### Async Parallel (v2.1.1)
```untold
start main() {
    // Fetch multiple URLs concurrently
    let results = await_all([
        http.get("https://api1.example.com"),
        http.get("https://api2.example.com"),
        http.get("https://api3.example.com")
    ])
    say(text(results))
}
```

---

**License**: MIT  
**Author**: Antony Jude  
**Version**: 2.1.1
