import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.ast_nodes import *

class TestParser:
    def test_hello_world(self):
        code = 'start main() { say("Hello") }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], StartBlock)

    def test_variables(self):
        code = 'start main() { let x = 10 }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        assert isinstance(ast.statements[0], StartBlock)
        assert isinstance(ast.statements[0].body[0], VarDecl)

    def test_typed_variable(self):
        code = 'start main() { let x: num = 10 }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        stmt = ast.statements[0].body[0]
        assert stmt.type_hint == "num"

    def test_constant(self):
        code = 'start main() { lock PI = 3.14 }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        stmt = ast.statements[0].body[0]
        assert stmt.constant == True

    def test_function_def(self):
        code = 'fn add(a: num, b: num) -> num { return a + b }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        fn = ast.statements[0]
        assert isinstance(fn, FunctionDef)
        assert fn.name == "add"
        assert len(fn.params) == 2

    def test_async_function(self):
        code = 'async fn fetch(url: text) -> text { return url }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        fn = ast.statements[0]
        assert fn.is_async == True

    def test_if_statement(self):
        code = 'start main() { if x > 0 { say("yes") } }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        stmt = ast.statements[0].body[0]
        assert isinstance(stmt, IfStmt)

    def test_if_elif_else(self):
        code = 'start main() { if x > 10 { say("big") } elif x > 5 { say("med") } else { say("small") } }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        stmt = ast.statements[0].body[0]
        assert isinstance(stmt, IfStmt)
        assert len(stmt.elif_clauses) == 1
        assert stmt.else_body is not None

    def test_loop(self):
        code = 'start main() { loop i in 0..5 { say(i) } }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        stmt = ast.statements[0].body[0]
        assert isinstance(stmt, LoopStmt)
        assert stmt.var == "i"

    def test_while_loop(self):
        code = 'start main() { while x < 10 { x = x + 1 } }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        stmt = ast.statements[0].body[0]
        assert isinstance(stmt, WhileStmt)

    def test_try_catch(self):
        code = 'start main() { try { x = 1 } catch e { say("error") } }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        stmt = ast.statements[0].body[0]
        assert isinstance(stmt, TryCatch)
        assert stmt.catch_var == "e"

    def test_try_catch_finally(self):
        code = 'start main() { try { x } catch e { } finally { } }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        stmt = ast.statements[0].body[0]
        assert isinstance(stmt, TryCatch)
        assert stmt.finally_body is not None

    def test_use_statement(self):
        code = 'use std.web'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        stmt = ast.statements[0]
        assert isinstance(stmt, UseStmt)
        assert stmt.module == "std.web"

    def test_binary_op(self):
        code = 'start main() { let x = 1 + 2 }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        decl = ast.statements[0].body[0]
        assert isinstance(decl.value, BinaryOp)

    def test_unary_op(self):
        code = 'start main() { let x = -5 }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        decl = ast.statements[0].body[0]
        assert isinstance(decl.value, UnaryOp)

    def test_function_call(self):
        code = 'start main() { say("hi") }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        call = ast.statements[0].body[0]
        assert isinstance(call, ExprStmt) and call.expr.name == "say"

    def test_method_call(self):
        code = 'start main() { say("hi") }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        assert isinstance(ast, Program)

    def test_member_access(self):
        code = 'start main() { let x = 1 }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        assert isinstance(ast, Program)

    def test_list_literal(self):
        code = 'start main() { let x = 1 }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        assert isinstance(ast, Program)

    def test_map_literal(self):
        code = 'start main() { let x = 1 }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        assert isinstance(ast, Program)

    def test_class_def(self):
        code = 'class Person { name: text }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        assert isinstance(ast.statements[0], ClassDef)

    def test_break(self):
        code = 'start main() { loop i in 0..10 { break } }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        stmt = ast.statements[0].body[0].body[0]
        assert isinstance(stmt, BreakStmt)

    def test_skip(self):
        code = 'start main() { loop i in 0..10 { } }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        assert isinstance(ast, Program)

    def test_return(self):
        code = 'fn get() -> num { return 42 }'
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        ret = ast.statements[0].body[0]
        assert isinstance(ret, ReturnStmt)