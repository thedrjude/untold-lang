import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.lexer.lexer       import Lexer
from src.parser.parser     import Parser
from src.interpreter.interpreter import Interpreter

def run(code):
    tokens = Lexer(code).tokenize()
    ast    = Parser(tokens).parse()
    Interpreter().run(ast)

print("=" * 40)
print("Test 1 — Hello World")
print("=" * 40)
run("""
start main() {
    say("Hello, Untold World!")
}
""")

print("\n" + "=" * 40)
print("Test 2 — Variables & arithmetic")
print("=" * 40)
run("""
start main() {
    let x = 10
    let y = 3
    say(x + y)
    say(x - y)
    say(x * y)
}
""")

print("\n" + "=" * 40)
print("Test 3 — If / elif / else")
print("=" * 40)
run("""
start main() {
    let score = 75
    if score >= 90 {
        say("Grade: A")
    } elif score >= 70 {
        say("Grade: B")
    } else {
        say("Grade: C")
    }
}
""")

print("\n" + "=" * 40)
print("Test 4 — Loop")
print("=" * 40)
run("""
start main() {
    loop i in 0..5 {
        say(i)
    }
}
""")

print("\n" + "=" * 40)
print("Test 5 — Functions")
print("=" * 40)
run("""
fn greet(name) {
    say("Hello, " + name + "!")
}

fn add(a, b) {
    return a + b
}

start main() {
    greet("Untold")
    let result = add(10, 20)
    say(result)
}
""")

print("\n" + "=" * 40)
print("Test 6 — Classes")
print("=" * 40)
run("""
class Person {
    name : text
    age  : num

    fn greet() {
        say("Hi, I am " + self.name)
    }
}

start main() {
    let p = Person{ name: "Dev", age: 22 }
    p.greet()
    say(p.name)
}
""")

print("\n" + "=" * 40)
print("Test 7 — Try / catch")
print("=" * 40)
run("""
start main() {
    try {
        let x = 10
        say("In try block")
    } catch err {
        say("Error: " + err.msg)
    } finally {
        say("Finally runs always")
    }
}
""")

print("\n" + "=" * 40)
print("Test 8 — Text methods")
print("=" * 40)
run("""
start main() {
    let msg = "untold lang"
    say(msg.upper())
    say(msg.length())
    say(msg.contains("lang"))
}
""")