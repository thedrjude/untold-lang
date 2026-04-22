# Untold Lang Roadmap

> The Language Without Limits · v2.1.1

---

## Phase 1: Core Language (Done ✓)

- [x] Lexer & Tokenizer
- [x] Parser with AST
- [x] Interpreter
- [x] Basic types (text, num, bool, list, map)
- [x] Variables (let, lock)
- [x] Functions (fn, return)
- [x] Control flow (if, elif, else, loop, while)
- [x] Error handling (try, catch, finally)
- [x] Entry point (start)
- [x] Standard library (12 modules)
- [x] Async/await support
- [x] Classes and objects
- [x] Native compilation (C backend)

---

## Phase 2: Language Features (Done ✓)

- [x] Async/await support (enhanced)
- [x] Classes and objects
- [x] Type annotations
- [x] Generics (partial)
- [ ] Pattern matching
- [ ] Enums
- [ ] Structs
- [ ] Closures

---

## Phase 3: Tools & Ecosystem (In Progress)

- [x] Package registry (20+ packages)
- [ ] Language server (LSP)
- [x] Debugger
- [x] REPL
- [ ] Formatter
- [ ] Linter
- [ ] Test framework
- [ ] Docs generator

---

## Phase 4: Performance (In Progress)

- [ ] JIT compilation
- [x] AOT compilation (C backend)
- [ ] Garbage collector
- [x] Native binaries
- [ ] WASM target

---

## Phase 5: Community

- [x] VS Code extension (published)
- [ ] Vim/Emacs plugins
- [x] Language spec document
- [ ] Tutorial docs
- [ ] Example projects
- [ ] Benchmark suite

---

## v2.1.1 Release — Security & Performance Update

### New Features

#### 1. Native Compilation (C Backend)
- Generate C code from Untold source
- Compile to native binaries for 10x performance
- Usage: `untold compile-c main.ut`

#### 2. Enhanced Security (Constant-Time Comparison)
- `crypto.secure_compare(a, b)` — timing-safe comparison
- `crypto.timing_safe_compare(a, b)` — cryptographic timing safety
- `crypto.verify_hash(password, hash, method)` — secure password verification
- `crypto.constant_time_compare(a, b)` — constant-time for sensitive data
- `hack.secure_compare(a, b)` — timing-safe comparison in hack module
- `hack.timing_safe_compare(a, b)` — timing-safe in hack module
- `hack.verify_hash(password, hash, method)` — verify hashes securely

#### 3. Improved Async Patterns
- `async_fn(fn)` — Create async function wrapper
- `await_all(promises)` — Await multiple promises
- `parallel(*fns)` — Run functions in parallel
- Enhanced `wait` for better async handling

#### 4. Expanded Package Ecosystem (20+ packages)
- `colors`, `uuid`, `dotenv`, `validator`, `logger`
- `date`, `math`, `csv`, `jsonwebtoken`, `bcrypt`
- `canvas`, `pdf`, `yaml`, `websocket`, `graphql`
- `compression`, `email`, `redis`, `mongo`, `cli`

---

## Release Schedule

| Version | Milestone | Target |
|---------|----------|--------|
| v0.1.0 | Initial release | Done |
| v0.1.1 | Async/await | Done |
| v0.1.2 | CI/CD fix | Done |
| v2.0.0 | Classes & literals | Done |
| v2.1.1 | Security & performance | Done |
| v2.2.0 | LSP & Debugger | TBD |
| v3.0.0 | WASM target | TBD |
| v1.0.0 | Stable release | TBD |

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.