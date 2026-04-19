# Every node in the AST inherits from Node
class Node:
    pass

# --- Statements ---

class Program(Node):
    def __init__(self, statements):
        self.statements = statements   # list of top-level statements

class StartBlock(Node):
    """start main() { ... }"""
    def __init__(self, name, params, body):
        self.name   = name
        self.params = params
        self.body   = body

class FunctionDef(Node):
    """fn add(a: num, b: num) -> num { ... }"""
    def __init__(self, name, params, return_type, body, is_async=False):
        self.name        = name
        self.params      = params        # list of (name, type) tuples
        self.return_type = return_type
        self.body        = body
        self.is_async    = is_async

class ClassDef(Node):
    """class Person { ... }"""
    def __init__(self, name, fields, methods):
        self.name    = name
        self.fields  = fields    # list of (name, type)
        self.methods = methods   # list of FunctionDef

class VarDecl(Node):
    """let x: num = 5   /   lock PI = 3.14"""
    def __init__(self, name, type_hint, value, constant=False):
        self.name     = name
        self.type_hint= type_hint
        self.value    = value
        self.constant = constant

class ReturnStmt(Node):
    def __init__(self, value):
        self.value = value

class IfStmt(Node):
    def __init__(self, condition, then_body, elif_clauses, else_body):
        self.condition    = condition
        self.then_body    = then_body
        self.elif_clauses = elif_clauses  # list of (condition, body)
        self.else_body    = else_body

class LoopStmt(Node):
    """loop i in 0..10 { ... }"""
    def __init__(self, var, start, end, body):
        self.var   = var
        self.start = start
        self.end   = end
        self.body  = body

class WhileStmt(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body      = body

class TryCatch(Node):
    def __init__(self, try_body, catch_var, catch_body, finally_body):
        self.try_body     = try_body
        self.catch_var    = catch_var
        self.catch_body   = catch_body
        self.finally_body = finally_body

class UseStmt(Node):
    """use untold.web"""
    def __init__(self, module):
        self.module = module

class BreakStmt(Node):
    pass

class SkipStmt(Node):
    pass

class ExprStmt(Node):
    """A statement that is just an expression, e.g. say("hi")"""
    def __init__(self, expr):
        self.expr = expr

class AssignStmt(Node):
    """x = 10"""
    def __init__(self, name, value):
        self.name  = name
        self.value = value

# --- Expressions ---

class NumberLiteral(Node):
    def __init__(self, value):
        self.value = value

class TextLiteral(Node):
    def __init__(self, value):
        self.value = value

class BoolLiteral(Node):
    def __init__(self, value):
        self.value = value

class NullLiteral(Node):
    pass

class Identifier(Node):
    def __init__(self, name):
        self.name = name

class BinaryOp(Node):
    """a + b, x == y, etc."""
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right

class UnaryOp(Node):
    """!x, -y"""
    def __init__(self, op, operand):
        self.op      = op
        self.operand = operand

class FunctionCall(Node):
    """say("hi") / add(1, 2)"""
    def __init__(self, name, args):
        self.name = name
        self.args = args

class MethodCall(Node):
    """p.greet() / http.get(url)"""
    def __init__(self, obj, method, args):
        self.obj    = obj
        self.method = method
        self.args   = args

class MemberAccess(Node):
    """self.name / person.age"""
    def __init__(self, obj, member):
        self.obj    = obj
        self.member = member

class RangeExpr(Node):
    """0..10"""
    def __init__(self, start, end):
        self.start = start
        self.end   = end

class ClassInstantiation(Node):
    """Person{ name: "Dev", age: 22 }"""
    def __init__(self, class_name, fields):
        self.class_name = class_name
        self.fields     = fields  # dict of name -> expr node
