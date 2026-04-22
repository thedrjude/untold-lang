# Untold Lang — Phase 1 Syntax Specification

> **The Language Without Limits** · `v2.2.0` · File extension: `.ut`

![version](https://img.shields.io/badge/version-v2.2.0-7C3AED)
![extension](https://img.shields.io/badge/extension-.ut-0F6E56)
![paradigm](https://img.shields.io/badge/paradigm-multi-185FA5)
![typing](https://img.shields.io/badge/typing-strong_%2B_inferred-854F0B)
![platforms](https://img.shields.io/badge/platforms-Linux_%7C_Windows_%7C_macOS-3B6D11)
![install](https://img.shields.io/badge/install-pip_install_untold--lang-993C1D)

---

## Identity

| Property | Value |
|----------|-------|
| Extension | `.ut` |
| Paradigm | Multi (imperative, OOP, async, functional) |
| Typing | Strong + inferred |
| Style | Readable & expressive |
| Platforms | Linux, Windows, macOS |
| Install | `pip install untold-lang` |
| Native Compilation | C backend |
| Security | Constant-time crypto |

---

## Hello World

```js
// main.ut — entry point of every Untold program
start main() {
    say("Hello, Untold World!")
}
```

---

## Variables & Types

```js
let name    = "Untold"        // inferred: text
let version : num  = 1.0      // explicitly typed
let active  : bool = true
lock PI     : num  = 3.14159  // constant (immutable)
```

### Built-in Types

| Type | Description | Example |
|------|-------------|---------|
| `text` | UTF-8 string | `"hello"` |
| `num` | Integer or float | `42`, `3.14` |
| `bool` | Boolean | `true`, `false` |
| `list` | Ordered array | `list(1, 2, 3)` |
| `map` | Key-value dictionary | `{key: value}` |
| `void` | No return value | — |
| `any` | Dynamic / unchecked | — |
| `byte` | Raw byte value | `0x41` |
| `func` | First-class function | — |
| `null` | Absence of value | `null` |

---

## Functions

```js
fn add(a: num, b: num) -> num {
    return a + b
}

// Async function (for AI, web calls)
async fn fetchData(url: text) -> text {
    wait result = http.get(url)
    return result.body
}
```

---

## Control Flow

```js
if x > 10 {
    say("big")
} elif x > 5 {
    say("medium")
} else {
    say("small")
}

loop i in 0..10 {        // range loop (0 to 9)
    say(i)
}

while active {           // while loop
    doWork()
}
```

### Loop Control

| Keyword | Behavior |
|---------|----------|
| `break` | Exit the current loop immediately |
| `skip` | Skip to next iteration (like `continue`) |

---

## Classes & Objects

```js
class Person {
    name : text
    age  : num

    fn greet() {
        say("Hi, I am " + self.name)
    }
}

let p = Person{ name: "Dev", age: 22 }
p.greet()
```

---

## Enums (v2.2.0)

```js
enum Status {
    Pending
    Active
    Done
}

let current = Status.Active
```

---

## Structs (v2.2.0)

```js
struct Point {
    x: num
    y: num
}

let p = Point{ x: 1, y: 2 }
say(p.x)
```

---

## Pattern Matching (v2.2.0)

```js
let result = match value {
    1 -> "one"
    2 -> "two"
    3 -> "three"
    else -> "other"
}
```

---

## String Templates (v2.2.0)

```js
let name = "World"
let msg = `Hello ${name}!`
say(msg)
```

---

## List Comprehensions (v2.2.0)

```js
// [x * x for x in 0..10 if x % 2 == 0]
let squares = [x * x for x in 0..10 if x % 2 == 0]
say(squares)
```

---

## Try Expressions (v2.2.0)

```js
// Elvis operator: value ?? default
let name = input_name ?? "Guest"
```

---

## Error Types (v2.2.0)

```js
try {
    throw MyError{ msg: "Oops!", code: 404 }
} catch err {
    say("Error: " + err.msg)
}
```

---

## Built-in Testing (v2.2.0)

```js
test "addition works" {
    assert_eq(add(2, 2), 4)
}

test "variables work" {
    let x = 10
    assert(x > 5)
}
```

---

## Modules & Imports

```js
use untold.ai       // AI / ML module
use untold.web      // Web / HTTP module
use untold.app      // Mobile & desktop UI
use untold.net      // Network & sockets
use untold.shell    // Scripting & system calls
use untold.hack     // Security & hacking tools
use untold.fs       // File system
use untold.db       // Database access
```

### Domain Modules

| Module | Purpose |
|--------|---------|
| ![](https://img.shields.io/badge/untold.ai-0F6E56?style=flat-square) | AI / ML — sentiment, keywords, summarize |
| ![](https://img.shields.io/badge/untold.web-185FA5?style=flat-square) | HTTP — GET, POST, web server |
| ![](https://img.shields.io/badge/untold.app-534AB7?style=flat-square) | Mobile & desktop UI |
| ![](https://img.shields.io/badge/untold.net-185FA5?style=flat-square) | Networking — ports, DNS, IP |
| ![](https://img.shields.io/badge/untold.hack-993C1D?style=flat-square) | Security — hashing, scanning, encoding |
| ![](https://img.shields.io/badge/untold.shell-3B6D11?style=flat-square) | Scripting — shell commands, env vars |
| ![](https://img.shields.io/badge/untold.fs-3B6D11?style=flat-square) | File system — read, write, delete |
| ![](https://img.shields.io/badge/untold.db-854F0B?style=flat-square) | Database access |

---

## Error Handling

```js
try {
    let data = fs.read("config.ut")
} catch err {
    say("Error: " + err.msg)
} finally {
    say("Done")
}
```

| Block | Purpose |
|-------|---------|
| `try` | Code that may throw an error |
| `catch err` | Runs if error is thrown — `err.msg` for message |
| `finally` | Always runs regardless of error |

---

## Standard Library

### untold.fs — File System

```js
use untold.fs

fs.write("file.txt", "hello")
let content = fs.read("file.txt")
fs.mkdir("myfolder")
fs.delete("file.txt")
say(fs.exists("file.txt"))
```

| Function | Signature | Description |
|----------|-----------|-------------|
| `fs.read` | `fs.read(path: text) -> text` | Read file contents |
| `fs.write` | `fs.write(path: text, data: text) -> void` | Write to file |
| `fs.mkdir` | `fs.mkdir(path: text) -> void` | Create directory |
| `fs.delete` | `fs.delete(path: text) -> void` | Delete file or directory |
| `fs.exists` | `fs.exists(path: text) -> bool` | Check if path exists |

---

### untold.web — HTTP

```js
use untold.web

let res = http.get("https://api.example.com/data")
say(res.status)
say(res.body)

http.serve(8080)
```

| Function | Signature | Description |
|----------|-----------|-------------|
| `http.get` | `http.get(url: text) -> Response` | HTTP GET request |
| `http.post` | `http.post(url: text, body: any) -> Response` | HTTP POST request |
| `http.serve` | `http.serve(port: num) -> void` | Start web server |

> `Response` object: `.status` (num) · `.body` (text) · `.headers` (map)

---

### untold.ai — Artificial Intelligence

```js
use untold.ai

let result  = ai.sentiment("This is amazing!")
let words   = ai.keywords(text, 5)
let summary = ai.summarize(text, 2)
```

| Function | Signature | Description |
|----------|-----------|-------------|
| `ai.sentiment` | `ai.sentiment(text: text) -> SentimentResult` | Analyze sentiment |
| `ai.keywords` | `ai.keywords(text: text, n: num) -> list` | Extract top n keywords |
| `ai.summarize` | `ai.summarize(text: text, n: num) -> text` | Summarize to N sentences |

> `SentimentResult`: `.label` (`"positive"` / `"negative"` / `"neutral"`) · `.score` (num)

---

### untold.shell — System & Scripting

```js
use untold.shell

let r = shell.run("ls -la")
say(r.out)
say(shell.platform())
say(shell.env("HOME"))
```

| Function | Signature | Description |
|----------|-----------|-------------|
| `shell.run` | `shell.run(cmd: text) -> ShellResult` | Run shell command |
| `shell.platform` | `shell.platform() -> text` | Get OS name |
| `shell.env` | `shell.env(key: text) -> text` | Get env variable |

> `ShellResult`: `.out` (text) · `.err` (text) · `.code` (num)

---

### untold.hack — Security Tools

```js
use untold.hack

say(hack.sha256("password"))
say(hack.b64_encode("hello"))
say(hack.port_scan("localhost", 80, 100))
say(hack.secure_compare("hash1", "hash2"))       // NEW: timing-safe compare
say(hack.timing_safe_compare(a, b))              // NEW: constant-time compare
say(hack.verify_hash("pass", "hash", "sha256"))  // NEW: verify with timing-safe
```

| Function | Signature | Description |
|----------|-----------|-------------|
| `hack.sha256` | `hack.sha256(data: text) -> text` | SHA-256 hash |
| `hack.b64_encode` | `hack.b64_encode(data: text) -> text` | Base64 encode |
| `hack.b64_decode` | `hack.b64_decode(data: text) -> text` | Base64 decode |
| `hack.port_scan` | `hack.port_scan(host: text, s: num, e: num) -> list` | Scan port range |
| `hack.secure_compare` | `hack.secure_compare(a: text, b: text) -> bool` | Constant-time compare |
| `hack.timing_safe_compare` | `hack.timing_safe_compare(a: text, b: text) -> bool` | Timing-safe comparison |
| `hack.verify_hash` | `hack.verify_hash(pwd: text, hash: text, method: text) -> bool` | Secure hash verification |

> **Note:** For ethical security research and authorized penetration testing only.

---

### untold.net — Networking

```js
use untold.net

let open = net.port_open("google.com", 443)
let ip   = net.resolve("google.com")
say(net.my_ip())
```

| Function | Signature | Description |
|----------|-----------|-------------|
| `net.port_open` | `net.port_open(host: text, port: num) -> bool` | Check if port is open |
| `net.resolve` | `net.resolve(host: text) -> text` | Resolve hostname to IP |
| `net.my_ip` | `net.my_ip() -> text` | Get local machine IP |

---

### untold.crypto — Cryptography Module

```js
use untold.crypto

say(crypto.sha256("password"))
say(crypto.sha512("data"))
say(crypto.hmac_sha256("key", "message"))
say(crypto.random_token(32))
say(crypto.secure_compare("a", "b"))              // NEW: timing-safe compare
say(crypto.timing_safe_compare(a, b))             // NEW: constant-time compare
say(crypto.verify_hash("pass", "hash"))           // NEW: secure verification
say(crypto.constant_time_compare(a, b))           // NEW: cryptographic constant-time
```

| Function | Signature | Description |
|----------|-----------|-------------|
| `crypto.sha256` | `crypto.sha256(data: text) -> text` | SHA-256 hash |
| `crypto.sha512` | `crypto.sha512(data: text) -> text` | SHA-512 hash |
| `crypto.blake2b` | `crypto.blake2b(data: text) -> text` | BLAKE2b hash |
| `crypto.hmac_sha256` | `crypto.hmac_sha256(key: text, msg: text) -> text` | HMAC-SHA256 |
| `crypto.hmac_sha512` | `crypto.hmac_sha512(key: text, msg: text) -> text` | HMAC-SHA512 |
| `crypto.random_token` | `crypto.random_token(len: num) -> text` | Random token generation |
| `crypto.random_bytes` | `crypto.random_bytes(len: num) -> text` | Random bytes |
| `crypto.secure_compare` | `crypto.secure_compare(a: text, b: text) -> bool` | Constant-time comparison |
| `crypto.timing_safe_compare` | `crypto.timing_safe_compare(a: text, b: text) -> bool` | Timing-safe comparison |
| `crypto.verify_hash` | `crypto.verify_hash(pwd: text, hash: text, method: text) -> bool` | Secure hash verification |
| `crypto.constant_time_compare` | `crypto.constant_time_compare(a: text, b: text) -> bool` | Constant-time for crypto |
| `crypto.pbkdf2` | `crypto.pbkdf2(pwd: text, salt: text, iter: num) -> text` | PBKDF2 key derivation |

---

## Complete Keyword Reference

| Keyword | Category | Description |
|---------|----------|-------------|
| `start` | Entry | Marks the program entry function |
| `fn` | Function | Declare a synchronous function |
| `async fn` | Function | Declare an asynchronous function |
| `return` | Function | Return a value |
| `wait` | Async | Await an async operation |
| `let` | Variable | Declare a mutable variable |
| `lock` | Variable | Declare an immutable constant |
| `class` | OOP | Declare a class |
| `enum` | OOP | Declare an enum type (v2.2.0) |
| `struct` | OOP | Declare a struct type (v2.2.0) |
| `self` | OOP | Reference to the current instance |
| `use` | Modules | Import a module |
| `if` | Control | Conditional branch |
| `elif` | Control | Else-if branch |
| `else` | Control | Default branch |
| `match` | Control | Pattern matching (v2.2.0) |
| `loop` | Control | Range / iterable for-loop |
| `while` | Control | Condition-based loop |
| `in` | Control | Iterator keyword (used with `loop`) |
| `break` | Control | Exit current loop |
| `skip` | Control | Skip to next iteration |
| `try` | Errors | Begin error-guarded block |
| `catch` | Errors | Handle thrown error |
| `finally` | Errors | Always-run cleanup block |
| `throw` | Errors | Throw custom error (v2.2.0) |
| `test` | Testing | Define a test block (v2.2.0) |
| `assert` | Testing | Assert condition (v2.2.0) |
| `assert_eq` | Testing | Assert equality (v2.2.0) |
| `yield` | Async | Yield value for iteration (v2.2.0) |
| `@` | Decorator | Decorator syntax (v2.2.0) |
| `??` | Operators | Elvis operator / null coalescing (v2.2.0) |
| `true` | Literals | Boolean true |
| `false` | Literals | Boolean false |
| `null` | Literals | No value |

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `untold run file.ut` | Run an Untold source file |
| `untold new <n> [template]` | Scaffold a new project |
| `untold build` | Build project to executable |
| `untold build --target binary` | Compile to standalone binary |
| `untold build --optimize 2` | Build with max optimization |
| `untold compile-c file.ut` | Compile to native C code (v2.1.1) |
| `untold check file.ut` | Check for syntax errors |
| `untold install <pkg>` | Install a package |
| `untold remove <pkg>` | Remove a package |
| `untold list` | List installed packages |
| `untold search <term>` | Search the package registry |
| `untold info` | Show project info |
| `untold repl` | Interactive REPL |
| `untold debug file.ut` | Debugger mode |

### Project Templates

| Template | Description |
|----------|-------------|
| `app` | General-purpose application |
| `web` | HTTP web server |
| `ai` | AI / ML project |
| `hack` | Security toolkit |
| `cli` | Command-line tool |
| `script` | Automation script |

---

## Complete Example — AI Web Scraper

```js
use untold.ai
use untold.web

start main() {
    // Fetch a web page
    let res      = http.get("https://example.com")

    // Run AI analysis on the response body
    let keywords = ai.keywords(res.body, 5)
    let mood     = ai.sentiment(res.body)

    // Output results
    say("Keywords: " + text(keywords))
    say("Sentiment: " + mood.label)
}
```

---

*Untold Lang v2.2.0 · [thedrjude.github.io/untold-lang](https://thedrjude.github.io/untold-lang) · The Language Without Limits*
