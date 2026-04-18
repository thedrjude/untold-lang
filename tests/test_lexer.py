import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.lexer.lexer import Lexer

code = """
start main() {
    let name = "Untold"
    let version: num = 1.0
    say(name)
}
"""

lexer  = Lexer(code)
tokens = lexer.tokenize()

for tok in tokens:
    print(tok)