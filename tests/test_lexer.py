import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.lexer.lexer import Lexer
from src.lexer.tokens import TokenType


class TestLexer:
    def test_hello_world(self):
        code = 'start main() { say("Hello") }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert len(tokens) > 0
        assert tokens[0].type == TokenType.START

    def test_numbers(self):
        code = 'start main() { let x = 42 }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        num_tokens = [t for t in tokens if t.type == TokenType.NUMBER]
        assert len(num_tokens) >= 1

    def test_strings(self):
        code = 'start main() { say("test") }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        str_tokens = [t for t in tokens if t.type == TokenType.TEXT]
        assert len(str_tokens) == 1
        assert str_tokens[0].value == "test"

    def test_operators(self):
        code = 'start main() { let x = 10 + 5 }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        op_tokens = [t for t in tokens if t.type == TokenType.PLUS]
        assert len(op_tokens) >= 1

    def test_identifiers(self):
        code = 'start main() { let name = "Untold" }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        id_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        assert len(id_tokens) >= 1

    def test_braces(self):
        code = 'start main() { }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert any(t.type == TokenType.LBRACE for t in tokens)
        assert any(t.type == TokenType.RBRACE for t in tokens)

    def test_parentheses(self):
        code = 'start main() { say("x") }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert any(t.type == TokenType.LPAREN for t in tokens)
        assert any(t.type == TokenType.RPAREN for t in tokens)

    def test_keywords(self):
        code = 'start main() { let x = 1 }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        keywords = [t.type for t in tokens if t.type in (
            TokenType.START, TokenType.LET, TokenType.FN, 
            TokenType.IF, TokenType.ELSE, TokenType.CLASS
        )]
        assert len(keywords) >= 1

    def test_true_false(self):
        code = 'start main() { let x = true }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert any(t.type == TokenType.TRUE for t in tokens)

    def test_loop_range(self):
        code = 'start main() { loop i in 0..5 { } }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert any(t.type == TokenType.DOTDOT for t in tokens)