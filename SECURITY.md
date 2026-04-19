# Security Policy

> How to report security vulnerabilities in Untold Lang v2.0.0

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:              |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **DO NOT** open a public GitHub issue
2. Email: thedrjude@github.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any fixes (if known)

## Scope

This security policy covers:
- The Untold Lang interpreter
- Standard library modules (`untold.hack`, `untold.crypto`, `untold.regex`, etc.)
- CLI commands (`untold run`, `untold repl`, `untold debug`)
- Package manager
- VS Code extension

**NOT covered:**
- Third-party packages from the registry
- User-written code using Untold Lang
- External services (APIs, databases, etc.)

## Disclosure

- Please give us reasonable time to fix before disclosure (30 days minimum)
- We appreciate credit in the fix (if desired)
- Security advisories will be published after the fix is released

---

## Security Best Practices

When using Untold Lang:

1. **Network modules** (`untold.net`, `untold.hack`) - Use only on systems you own or have authorization
2. **Crypto module** - For educational purposes; use established libraries for production
3. **Shell execution** - Be cautious with user input
4. **File system** - Validate all paths to prevent directory traversal

---

_Thank you for helping keep Untold Lang secure!_