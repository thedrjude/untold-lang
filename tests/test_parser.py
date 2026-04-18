import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.ast_nodes import *

code = """
start main() {
    let name = "Untold"
    let version: num = 1.0
    say(name)
    if version > 0.5 {
        say("Ready!")
    }
    loop i in 0..3 {
        say(i)
    }
}
"""

tokens = Lexer(code).tokenize()
ast    = Parser(tokens).parse()

def print_ast(node, indent=0):
    pad = "  " * indent
    prefix = f"{pad}{node.__class__.__name__}"

    if isinstance(node, Program):
        print(f"{prefix}  [{len(node.statements)} statements]")
        for s in node.statements:
            print_ast(s, indent + 1)

    elif isinstance(node, StartBlock):
        print(f"{prefix}  name='{node.name}'  params={node.params}")
        for s in node.body:
            print_ast(s, indent + 1)

    elif isinstance(node, FunctionDef):
        print(f"{prefix}  name='{node.name}'  params={node.params}  returns={node.return_type}  async={node.is_async}")
        for s in node.body:
            print_ast(s, indent + 1)

    elif isinstance(node, VarDecl):
        kind = "lock" if node.constant else "let"
        print(f"{prefix}  [{kind}]  name='{node.name}'  type={node.type_hint}")
        print_ast(node.value, indent + 1)

    elif isinstance(node, AssignStmt):
        print(f"{prefix}  name='{node.name}'")
        print_ast(node.value, indent + 1)

    elif isinstance(node, ReturnStmt):
        print(f"{prefix}")
        print_ast(node.value, indent + 1)

    elif isinstance(node, ExprStmt):
        print(f"{prefix}")
        print_ast(node.expr, indent + 1)

    elif isinstance(node, IfStmt):
        print(f"{prefix}")
        print(f"{pad}  [condition]")
        print_ast(node.condition, indent + 2)
        print(f"{pad}  [then]")
        for s in node.then_body:
            print_ast(s, indent + 2)
        for (ec, eb) in node.elif_clauses:
            print(f"{pad}  [elif]")
            print_ast(ec, indent + 2)
            for s in eb:
                print_ast(s, indent + 2)
        if node.else_body:
            print(f"{pad}  [else]")
            for s in node.else_body:
                print_ast(s, indent + 2)

    elif isinstance(node, LoopStmt):
        print(f"{prefix}  var='{node.var}'")
        print(f"{pad}  [start]")
        print_ast(node.start, indent + 2)
        print(f"{pad}  [end]")
        print_ast(node.end, indent + 2)
        print(f"{pad}  [body]")
        for s in node.body:
            print_ast(s, indent + 2)

    elif isinstance(node, WhileStmt):
        print(f"{prefix}")
        print(f"{pad}  [condition]")
        print_ast(node.condition, indent + 2)
        print(f"{pad}  [body]")
        for s in node.body:
            print_ast(s, indent + 2)

    elif isinstance(node, TryCatch):
        print(f"{prefix}  catch_var='{node.catch_var}'")
        print(f"{pad}  [try]")
        for s in node.try_body:
            print_ast(s, indent + 2)
        if node.catch_body:
            print(f"{pad}  [catch]")
            for s in node.catch_body:
                print_ast(s, indent + 2)
        if node.finally_body:
            print(f"{pad}  [finally]")
            for s in node.finally_body:
                print_ast(s, indent + 2)

    elif isinstance(node, UseStmt):
        print(f"{prefix}  module='{node.module}'")

    elif isinstance(node, FunctionCall):
        print(f"{prefix}  name='{node.name}'  [{len(node.args)} args]")
        for a in node.args:
            print_ast(a, indent + 1)

    elif isinstance(node, MethodCall):
        print(f"{prefix}  method='{node.method}'  [{len(node.args)} args]")
        print_ast(node.obj, indent + 1)
        for a in node.args:
            print_ast(a, indent + 1)

    elif isinstance(node, MemberAccess):
        print(f"{prefix}  member='{node.member}'")
        print_ast(node.obj, indent + 1)

    elif isinstance(node, BinaryOp):
        print(f"{prefix}  op='{node.op}'")
        print_ast(node.left,  indent + 1)
        print_ast(node.right, indent + 1)

    elif isinstance(node, UnaryOp):
        print(f"{prefix}  op='{node.op}'")
        print_ast(node.operand, indent + 1)

    elif isinstance(node, NumberLiteral):
        print(f"{prefix}  value={node.value}")

    elif isinstance(node, TextLiteral):
        print(f"{prefix}  value='{node.value}'")

    elif isinstance(node, BoolLiteral):
        print(f"{prefix}  value={node.value}")

    elif isinstance(node, NullLiteral):
        print(f"{prefix}  value=null")

    elif isinstance(node, Identifier):
        print(f"{prefix}  name='{node.name}'")

    elif isinstance(node, BreakStmt):
        print(f"{prefix}")

    elif isinstance(node, SkipStmt):
        print(f"{prefix}")

    else:
        print(f"{prefix}  [unhandled node type]")

print_ast(ast)