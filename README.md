<div align="center">

# Untold Lang v2.0.0

**The Language Without Limits** — Version 2.0.0

[![Version](https://img.shields.io/pypi/v/untold-lang/2.0.0?style=flat&color=a78bfa)](https://pypi.org/project/untold-lang/2.0.0/)
[![License](https://img.shields.io/badge/license-MIT-34d399)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-60a5fa)](https://github.com/thedrjude/untold-lang.git)
[![Test Status](https://img.shields.io/github/actions/workflow/status/thedrjude/untold-lang/test?label=Tests)](https://github.com/thedrjude/untold-lang/actions)
[![Downloads](https://img.shields.io/pypi/dm/untold-lang?style=flat)](https://pypi.org/project/untold-lang/)
[![Python Version](https://img.shields.io/pypi/pyversions/untold-lang)](https://pypi.org/project/untold-lang/)

[Website](https://untold-lang.github.io) · [PyPI](https://pypi.org/project/untold-lang/2.0.0/) · [Discussions](https://github.com/thedrjude/untold-lang/discussions)

</div>

---

## What is Untold Lang?

**Untold Lang v2.0.0** is a powerful, expressive programming language built for **AI, Web, Apps, Scripting, Security** and more — all with one clean syntax and file extension `.ut`.

## Try It Now

```bash
pip install untold-lang==2.0.0
untold new my-app
cd my-app
untold run main.ut
```

## What's New in v2.0.0

- **List Literals**: `[1, 2, 3]`
- **Map Literals**: `{"name": "Dev", "age": 22}`
- **REPL Mode**: `untold repl` or `untold shell`
- **Debugger**: `untold debug <file.ut>`
- **New Modules**: `untold.regex`, `untold.time`, `untold.crypto`
- **Better Error Messages**

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

## Standard Library (11 Modules)

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
| `untold.crypto` | Cryptographic functions |
| `untold.db` | Database access |
| `untold.app` | Desktop & mobile UI |

## CLI Commands

```bash
untold run main.ut              # Run a .ut file
untold repl                    # Interactive REPL
untold debug main.ut           # Start debugger
untold new my-app web          # Create project
untold build --target binary   # Compile to binary
untold install colors uuid    # Install packages
untold check main.ut          # Check syntax
untold help                  # All commands
```

## Code Example

```untold
start main() {
    // New in v2.0.0 - List and Map literals
    let items = [1, 2, 3, 4, 5]
    let data = {"name": "Untold Lang", "version": "2.0.0"}
    
    say("Items: " + text(items.length()))
    say("Name: " + data.get("name"))
    
    // Use regex module
    use untold.regex
    let found = regex.match("\\d+", "version 2.0")
    say("Found: " + found)
}
```

---

**License**: MIT  
**Author**: Antony Jude  
**Version**: 2.0.0
