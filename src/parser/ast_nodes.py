# Every node in the AST inherits from Node
class Node:
    pass

# --- Statements ---

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class StartBlock(Node):
    """start main() { ... }"""
    def __init__(self, name, params, body):
        self.name   = name
        self.params = params
        self.body   = body

class FunctionDef(Node):
    """fn add(a: num, b: num) -> num { ... }"""
    def __init__(self, name, params, return_type, body, is_async=False, decorators=None):
        self.name        = name
        self.params      = params
        self.return_type = return_type
        self.body        = body
        self.is_async    = is_async
        self.decorators  = decorators or []

class ClassDef(Node):
    """class Person { ... }"""
    def __init__(self, name, fields, methods):
        self.name    = name
        self.fields  = fields
        self.methods = methods

# 1. ENUM Type
class EnumDef(Node):
    """enum Status { Pending, Active, Done }"""
    def __init__(self, name, variants):
        self.name    = name
        self.variants = variants  # list of variant names

# 2. STRUCT Type
class StructDef(Node):
    """struct Point { x: num, y: num }"""
    def __init__(self, name, fields):
        self.name   = name
        self.fields = fields  # list of (name, type)

class VarDecl(Node):
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
        self.elif_clauses = elif_clauses
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

# 3. THROW Statement
class ThrowStmt(Node):
    """throw MyError{ msg: "Oops", code: 404 }"""
    def __init__(self, error_name, fields):
        self.error_name = error_name
        self.fields     = fields

class UseStmt(Node):
    """use untold.web"""
    def __init__(self, module):
        self.module = module

class BreakStmt(Node):
    pass

class SkipStmt(Node):
    pass

class ExprStmt(Node):
    def __init__(self, expr):
        self.expr = expr

class AssignStmt(Node):
    def __init__(self, name, value):
        self.name  = name
        self.value = value

# 4. TEST Block
class TestBlock(Node):
    """test "addition works" { assert_eq(add(2,2), 4) }"""
    def __init__(self, name, body):
        self.name = name
        self.body = body

# 9. YIELD Statement (for async iterators)
class YieldStmt(Node):
    """yield value"""
    def __init__(self, value):
        self.value = value

# --- Expressions ---

class NumberLiteral(Node):
    def __init__(self, value):
        self.value = value

class TextLiteral(Node):
    def __init__(self, value):
        self.value = value

# 5. String Template
class TextTemplate(Node):
    """`Hello ${name}!`"""
    def __init__(self, parts):
        # parts is list of (is_variable: bool, value: str)
        self.parts = parts

class BoolLiteral(Node):
    def __init__(self, value):
        self.value = value

class NullLiteral(Node):
    pass

class Identifier(Node):
    def __init__(self, name):
        self.name = name

class BinaryOp(Node):
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right

class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op      = op
        self.operand = operand

class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class MethodCall(Node):
    def __init__(self, obj, method, args):
        self.obj    = obj
        self.method = method
        self.args   = args

class MemberAccess(Node):
    def __init__(self, obj, member):
        self.obj    = obj
        self.member = member

class RangeExpr(Node):
    def __init__(self, start, end):
        self.start = start
        self.end   = end

class ClassInstantiation(Node):
    """Person{ name: "Dev", age: 22 }"""
    def __init__(self, class_name, fields):
        self.class_name = class_name
        self.fields     = fields

class ListLiteral(Node):
    def __init__(self, elements):
        self.elements = elements

# 6. List Comprehension
class ListComprehension(Node):
    """[x * x for x in 0..10 if x % 2 == 0]"""
    def __init__(self, expr, var, iterable, condition):
        self.expr      = expr
        self.var       = var
        self.iterable  = iterable
        self.condition = condition

class MapLiteral(Node):
    def __init__(self, pairs):
        self.pairs = pairs

# 7. Struct Instantiation
class StructInstantiation(Node):
    """Point{ x: 1, y: 2 }"""
    def __init__(self, struct_name, fields):
        self.struct_name = struct_name
        self.fields      = fields

# 8. Pattern Matching
class MatchExpr(Node):
    """match value { 1 -> "one", 2 -> "two", else -> "other" }"""
    def __init__(self, value, cases, default):
        self.value   = value
        self.cases   = cases  # list of (pattern, result)
        self.default = default

# 10. Elvis/Elvis Operator (null coalescing)
class ElvisOp(Node):
    """value ?? default"""
    def __init__(self, left, right):
        self.left  = left
        self.right = right

# 10. Assert Expression
class AssertExpr(Node):
    """assert(condition)"""
    def __init__(self, condition, message=None):
        self.condition = condition
        self.message  = message

class AssertEqExpr(Node):
    """assert_eq(a, b)"""
    def __init__(self, left, right):
        self.left  = left
        self.right = right