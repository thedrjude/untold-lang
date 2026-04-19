# Contributing to Untold Lang

> The Language Without Limits

Thank you for your interest in contributing to Untold Lang! This guide will help you get started.

---

## Code of Conduct

By participating, you agree to follow our [Code of Conduct](./CODE_OF_CONDUCT.md).

---

## How Can I Contribute?

### Report Bugs

1. Check [Issues](https://github.com/thedrjude/untold-lang/issues) for existing reports
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)

### Suggest Features

1. Search [Issues](https://github.com/thedrjude/untold-lang/issues) first
2. Open a discussion in [Discussions](https://github.com/thedrjude/untold-lang/discussions)
3. Use the "Feature Request" template

### Pull Requests

#### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/untold-lang.git
cd untold-lang

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .
pip install pytest

# Run tests
pytest tests/ -v
```

#### Coding Standards

- Use 4 spaces for indentation
- Max line length: 100 characters
- Add tests for new features
- Update documentation

#### PR Process

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `pytest tests/ -v`
4. Commit with clear messages
5. Push and open a PR

---

## Project Structure

```
untold-lang/
├── cli/           # Command-line interface
├── src/
│   ├── lexer/    # Tokenizer
│   ├── parser/   # AST parser
│   ├── interpreter/  # Interpreter
│   └── compiler/ # Compiler (WIP)
├── stdlib/       # Standard library
│   ├── ai.py    # AI module
│   ├── web.py   # Web module
│   ├── fs.py    # File system
│   └── ...
└── tests/       # Test suite
```

---

## Commit Messages

- Use imperative mood: "Add feature" not "Added feature"
- Keep first line under 72 characters
- Reference issues: "Fix #123"

---

## Recognition

All contributors will be added to CONTRIBUTORS.md.

---

## Questions?

Open a [Discussion](https://github.com/thedrjude/untold-lang/discussions) or join our community.