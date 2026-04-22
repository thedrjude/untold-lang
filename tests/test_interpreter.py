import os
import sys
from contextlib import redirect_stdout
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.interpreter.interpreter import Interpreter
from src.lexer.lexer import Lexer
from src.parser.parser import Parser


def run_code(code, expected_output=None):
    tokens = Lexer(code).tokenize()
    ast = Parser(tokens).parse()
    interpreter = Interpreter()
    
    if expected_output is not None:
        f = StringIO()
        with redirect_stdout(f):
            interpreter.run(ast)
        output = f.getvalue().strip()
        assert expected_output in output, f"Expected '{expected_output}' but got '{output}'"
    else:
        interpreter.run(ast)

class TestHelloWorld:
    def test_say_hello(self):
        run_code('start main() { say("Hello World") }', "Hello World")

class TestVariables:
    def test_let_number(self):
        run_code('start main() { let x = 10 }')
    
    def test_let_string(self):
        run_code('start main() { let name = "Untold" }')
    
    def test_let_boolean(self):
        run_code('start main() { let active = true }')

class TestArithmetic:
    def test_addition(self):
        run_code('start main() { let x = 10 + 5 }')
    
    def test_subtraction(self):
        run_code('start main() { let x = 10 - 5 }')
    
    def test_multiplication(self):
        run_code('start main() { let x = 3 * 4 }')
    
    def test_division(self):
        run_code('start main() { let x = 10 / 2 }')

class TestControlFlow:
    def test_if(self):
        run_code('start main() { if true { say("yes") } }', "yes")
    
    def test_if_else(self):
        run_code('start main() { if false { say("yes") } else { say("no") } }', "no")

class TestLoops:
    def test_loop_range(self):
        run_code('start main() { loop i in 0..3 { } }')

class TestFunctions:
    def test_function_call(self):
        code = 'fn add(a, b) { return a + b }\nstart main() { let x = add(2, 3) }'
        run_code(code)

class TestErrorHandling:
    def test_try_catch(self):
        code = 'start main() { try { say("ok") } catch err { say(err.msg) } }'
        run_code(code, "ok")

class TestLock:
    def test_lock_constant(self):
        code = 'start main() { lock PI = 3.14 }'
        run_code(code)

class TestKeywords:
    def test_true(self):
        run_code('start main() { let x = true }')
    
    def test_false(self):
        run_code('start main() { let x = false }')
    
    def test_null(self):
        run_code('start main() { let x = null }')