import asyncio

from src.parser.ast_nodes import *

from .environment import Environment


class ReturnSignal(Exception):
    def __init__(self, value): self.value = value

class BreakSignal(Exception):
    pass

class SkipSignal(Exception):
    pass

class UntoldFunction:
    def __init__(self, node, closure):
        self.node    = node
        self.closure = closure

    def __repr__(self):
        return f"<fn {self.node.name}>"

class UntoldInstance:
    def __init__(self, class_def, fields):
        self.class_def = class_def
        self.fields    = fields

    def get(self, name):
        if name in self.fields:
            return self.fields[name]
        raise AttributeError(f"[Untold] '{self.class_def.name}' has no member '{name}'")

    def set(self, name, value):
        self.fields[name] = value

    def __repr__(self):
        return f"<{self.class_def.name} {self.fields}>"

class UntoldEnum:
    def __init__(self, name, variants):
        self.name = name
        self.variants = {v: i for i, v in enumerate(variants)}

    def __repr__(self):
        return f"<enum {self.name} {list(self.variants.keys())}>"

class UntoldStruct:
    def __init__(self, name, fields):
        self.name = name
        self.field_names = [f[0] for f in fields]

    def __repr__(self):
        return f"<struct {self.name}>"

class UntoldError(Exception):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
        self.msg = fields.get("msg", f"{name} error")

class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self._load_builtins()
        self._test_results = []

    def _load_builtins(self):
        g = self.globals

        def builtin_say(*args):
            print(*[self._stringify(a) for a in args])

        def builtin_ask(prompt=""):
            return input(self._stringify(prompt))

        def builtin_len(val):
            if isinstance(val, (str, list)):
                return len(val)
            raise TypeError(f"[Untold] len() expects text or list, got {type(val)}")

        def builtin_type(val):
            mapping = {
                int: "num", float: "num", str: "text",
                bool: "bool", list: "list", dict: "map",
                type(None): "null"
            }
            return mapping.get(type(val), "unknown")

        def builtin_num(val):
            try:
                return float(val) if "." in str(val) else int(val)
            except:
                raise ValueError(f"[Untold] Cannot convert '{val}' to num")

        def builtin_text(val):
            return self._stringify(val)

        def builtin_list(*args):
            return list(args) if args else []

        def builtin_range(start, end):
            return list(range(int(start), int(end)))

        async def builtin_wait(promise):
            if asyncio.iscoroutine(promise):
                return await promise
            if hasattr(promise, '__await__'):
                return promise.__await__()
            return promise

        def builtin_async(fn, *args):
            if asyncio.iscoroutinefunction(fn):
                return fn(*args)
            return fn(*args)

        def builtin_await_all(promises):
            if isinstance(promises, list):
                return asyncio.gather(*[asyncio.to_thread(p) if not asyncio.iscoroutine(p) else p for p in promises])
            return promises

        def builtin_parallel(*fns):
            async def run_all():
                tasks = []
                for fn in fns:
                    if asyncio.iscoroutinefunction(fn):
                        tasks.append(fn())
                    else:
                        tasks.append(asyncio.to_thread(fn))
                return await asyncio.gather(*tasks)
            return asyncio.run(run_all())

        def builtin_assert(condition, message="Assertion failed"):
            if not condition:
                raise AssertionError(f"[Untold] {message}")

        def builtin_assert_eq(left, right):
            if left != right:
                raise AssertionError(f"[Untold] assert_eq failed: {left} != {right}")

        def builtin_match(value, cases, default):
            for pattern, result in cases:
                if self._eval_simple(value) == self._eval_simple(pattern):
                    return self.eval(result, self.globals)
            if default:
                return self.eval(default, self.globals)
            return None

        g.set("say",   builtin_say)
        g.set("wait",  builtin_wait)
        g.set("async_fn", builtin_async)
        g.set("await_all", builtin_await_all)
        g.set("parallel", builtin_parallel)
        g.set("assert", builtin_assert)
        g.set("assert_eq", builtin_assert_eq)
        g.set("match", builtin_match)
        g.set("ask",   builtin_ask)
        g.set("len",   builtin_len)
        g.set("type",  builtin_type)
        g.set("num",   builtin_num)
        g.set("text",  builtin_text)
        g.set("list",  builtin_list)
        g.set("range", builtin_range)

    def _eval_simple(self, node):
        if isinstance(node, NumberLiteral):
            return node.value
        if isinstance(node, TextLiteral):
            return node.value
        if isinstance(node, Identifier):
            return self.globals.get(node.name)
        return node

    def _stringify(self, val):
        if isinstance(val, bool):
            return "true" if val else "false"
        if val is None:
            return "null"
        if isinstance(val, float) and val == int(val):
            return str(int(val))
        return str(val)

    def run(self, program: Program):
        env = self.globals
        tests = []

        for stmt in program.statements:
            if isinstance(stmt, (FunctionDef, ClassDef, UseStmt, EnumDef, StructDef)):
                self.exec(stmt, env)

        for stmt in program.statements:
            if isinstance(stmt, TestBlock):
                tests.append(stmt)

        for stmt in program.statements:
            if isinstance(stmt, StartBlock):
                self.exec(stmt, env)
                return

        for stmt in program.statements:
            if not isinstance(stmt, (FunctionDef, ClassDef, UseStmt, EnumDef, StructDef, TestBlock)):
                self.exec(stmt, env)

        if tests:
            self._run_tests(tests, env)

    def _run_tests(self, tests, env):
        passed = 0
        failed = 0
        say("=" * 40)
        say("Running tests...")
        say("=" * 40)
        for test in tests:
            try:
                local = Environment(parent=env)
                self.exec_block(test.body, local)
                say(f"  PASS: {test.name}")
                passed += 1
            except Exception as e:
                say(f"  FAIL: {test.name} - {e}")
                failed += 1
        say("=" * 40)
        say(f"Results: {passed} passed, {failed} failed")
        say("=" * 40)

    def exec(self, node, env):
        if isinstance(node, StartBlock):
            local = Environment(parent=env)
            self.exec_block(node.body, local)

        elif isinstance(node, FunctionDef):
            fn = UntoldFunction(node, env)
            env.set(node.name, fn)

        elif isinstance(node, ClassDef):
            env.set(node.name, node)

        elif isinstance(node, EnumDef):
            env.set(node.name, UntoldEnum(node.name, node.variants))

        elif isinstance(node, StructDef):
            env.set(node.name, UntoldStruct(node.name, node.fields))

        elif isinstance(node, UseStmt):
            self._load_module(node.module, env)

        elif isinstance(node, VarDecl):
            value = self.eval(node.value, env)
            if node.constant:
                env.set_constant(node.name, value)
            else:
                env.set(node.name, value)

        elif isinstance(node, AssignStmt):
            if env.is_constant(node.name):
                raise RuntimeError(f"[Untold] Cannot reassign constant '{node.name}'")
            value = self.eval(node.value, env)
            env.assign(node.name, value)

        elif isinstance(node, ReturnStmt):
            raise ReturnSignal(self.eval(node.value, env))

        elif isinstance(node, ThrowStmt):
            fields = {k: self.eval(v, env) for k, v in node.fields.items()}
            raise UntoldError(node.error_name, fields)

        elif isinstance(node, YieldStmt):
            raise ReturnSignal(self.eval(node.value, env))

        elif isinstance(node, IfStmt):
            if self.eval(node.condition, env):
                self.exec_block(node.then_body, Environment(parent=env))
            else:
                ran = False
                for (ec, eb) in node.elif_clauses:
                    if self.eval(ec, env):
                        self.exec_block(eb, Environment(parent=env))
                        ran = True
                        break
                if not ran and node.else_body:
                    self.exec_block(node.else_body, Environment(parent=env))

        elif isinstance(node, LoopStmt):
            start = int(self.eval(node.start, env))
            end   = int(self.eval(node.end,   env))
            for i in range(start, end):
                local = Environment(parent=env)
                local.set(node.var, i)
                try:
                    self.exec_block(node.body, local)
                except BreakSignal:
                    break
                except SkipSignal:
                    continue

        elif isinstance(node, WhileStmt):
            while self.eval(node.condition, env):
                local = Environment(parent=env)
                try:
                    self.exec_block(node.body, local)
                except BreakSignal:
                    break
                except SkipSignal:
                    continue

        elif isinstance(node, TryCatch):
            try:
                self.exec_block(node.try_body, Environment(parent=env))
            except UntoldError as e:
                if node.catch_body:
                    local = Environment(parent=env)
                    err_obj = {"msg": e.msg, "type": e.name}
                    local.set(node.catch_var, err_obj)
                    self.exec_block(node.catch_body, local)
            except Exception as e:
                if node.catch_body:
                    local = Environment(parent=env)
                    err_obj = {"msg": str(e), "type": type(e).__name__}
                    local.set(node.catch_var, err_obj)
                    self.exec_block(node.catch_body, local)
            finally:
                if node.finally_body:
                    self.exec_block(node.finally_body, Environment(parent=env))

        elif isinstance(node, BreakStmt):
            raise BreakSignal()

        elif isinstance(node, SkipStmt):
            raise SkipSignal()

        elif isinstance(node, ExprStmt):
            self.eval(node.expr, env)

        else:
            raise RuntimeError(f"[Untold] Unknown statement: {type(node).__name__}")

    def exec_block(self, stmts, env):
        for stmt in stmts:
            self.exec(stmt, env)

    def eval(self, node, env):
        if isinstance(node, NumberLiteral):
            return node.value

        elif isinstance(node, TextLiteral):
            return node.value

        elif isinstance(node, TextTemplate):
            result = ""
            for is_var, val in node.parts:
                if is_var:
                    result += self._stringify(env.get(val))
                else:
                    result += val
            return result

        elif isinstance(node, BoolLiteral):
            return node.value

        elif isinstance(node, NullLiteral):
            return None

        elif isinstance(node, Identifier):
            return env.get(node.name)

        elif isinstance(node, BinaryOp):
            left  = self.eval(node.left,  env)
            right = self.eval(node.right, env)
            op    = node.op
            if op in ("PLUS", "+"):
                if isinstance(left, str) or isinstance(right, str):
                    return self._stringify(left) + self._stringify(right)
                return left + right
            elif op in ("MINUS", "-"):
                return left - right
            elif op in ("STAR", "*"):
                return left * right
            elif op in ("SLASH", "/"):
                if right == 0:
                    raise ZeroDivisionError("[Untold] Division by zero")
                return left / right
            elif op in ("PERCENT", "%"):
                return left % right
            elif op in ("EQEQ", "=="):
                return left == right
            elif op in ("NEQ", "!="):
                return left != right
            elif op in ("LT", "<"):
                return left < right
            elif op in ("GT", ">"):
                return left > right
            elif op in ("LTE", "<="):
                return left <= right
            elif op in ("GTE", ">="):
                return left >= right
            elif op in ("AND", "&&"):
                return bool(left) and bool(right)
            elif op in ("OR", "||"):
                return bool(left) or bool(right)
            else:
                raise RuntimeError(f"[Untold] Unknown operator '{op}'")

        elif isinstance(node, UnaryOp):
            val = self.eval(node.operand, env)
            if node.op in ("NOT", "!"):
                return not val
            if node.op in ("MINUS", "-"):
                return -val

        elif isinstance(node, ElvisOp):
            left = self.eval(node.left, env)
            if left is None or left == "":
                return self.eval(node.right, env)
            return left

        elif isinstance(node, FunctionCall):
            fn   = env.get(node.name)
            args = [self.eval(a, env) for a in node.args]
            return self._call(fn, args, env)

        elif isinstance(node, MethodCall):
            obj  = self.eval(node.obj, env)
            args = [self.eval(a, env) for a in node.args]
            return self._method_call(obj, node.method, args, env)

        elif isinstance(node, MemberAccess):
            obj = self.eval(node.obj, env)
            if isinstance(obj, UntoldInstance):
                return obj.get(node.member)
            if isinstance(obj, dict):
                return obj.get(node.member)
            if isinstance(obj, UntoldStruct):
                return None
            raise AttributeError(f"[Untold] Cannot access member '{node.member}'")

        elif isinstance(node, ClassInstantiation):
            class_def = env.get(node.class_name)
            if isinstance(class_def, UntoldStruct):
                evaluated_fields = {k: self.eval(v, env) for k, v in node.fields.items()}
                return StructInstance(class_def, evaluated_fields)
            if not isinstance(class_def, ClassDef):
                raise TypeError(f"[Untold] '{node.class_name}' is not a class")
            evaluated_fields = {k: self.eval(v, env) for k, v in node.fields.items()}
            return UntoldInstance(class_def, evaluated_fields)

        elif isinstance(node, ListLiteral):
            return [self.eval(e, env) for e in node.elements]

        elif isinstance(node, ListComprehension):
            result = []
            iterable = self.eval(node.iterable, env)
            for item in iterable:
                local = Environment(parent=env)
                local.set(node.var, item)
                if node.condition:
                    if not self.eval(node.condition, local):
                        continue
                result.append(self.eval(node.expr, local))
            return result

        elif isinstance(node, MapLiteral):
            return {k: self.eval(v, env) for k, v in node.pairs.items()}

        elif isinstance(node, StructInstantiation):
            struct_def = env.get(node.struct_name)
            if not isinstance(struct_def, UntoldStruct):
                raise TypeError(f"[Untold] '{node.struct_name}' is not a struct")
            evaluated_fields = {k: self.eval(v, env) for k, v in node.fields.items()}
            return StructInstance(struct_def, evaluated_fields)

        elif isinstance(node, MatchExpr):
            value = self.eval(node.value, env)
            for pattern, result in node.cases:
                pat_val = self.eval(pattern, env)
                if value == pat_val:
                    return self.eval(result, env)
            if node.default:
                return self.eval(node.default, env)
            return None

        elif isinstance(node, AssertExpr):
            cond = self.eval(node.condition, env)
            if not cond:
                raise AssertionError("[Untold] assert failed")

        elif isinstance(node, AssertEqExpr):
            left = self.eval(node.left, env)
            right = self.eval(node.right, env)
            if left != right:
                raise AssertionError(f"[Untold] assert_eq failed: {left} != {right}")

        else:
            raise RuntimeError(f"[Untold] Unknown expression: {type(node).__name__}")

    def _call(self, fn, args, env):
        if callable(fn) and not isinstance(fn, UntoldFunction):
            return fn(*args)

        if not isinstance(fn, UntoldFunction):
            raise TypeError(f"[Untold] '{fn}' is not callable")

        node  = fn.node
        local = Environment(parent=fn.closure)

        for i, (pname, _ptype) in enumerate(node.params):
            local.set(pname, args[i] if i < len(args) else None)

        if node.is_async:
            async def run_async():
                try:
                    self.exec_block(node.body, local)
                except ReturnSignal as r:
                    return r.value
                return None
            return asyncio.run(run_async())

        try:
            self.exec_block(node.body, local)
        except ReturnSignal as r:
            return r.value
        return None

    def _method_call(self, obj, method, args, env):
        import inspect
        if inspect.isclass(obj):
            fn = getattr(obj, method, None)
            if fn:
                return fn(*args)
            raise AttributeError(f"[Untold] Module has no method '{method}'")
        if isinstance(obj, str):
            if method == "upper":    return obj.upper()
            if method == "lower":    return obj.lower()
            if method == "trim":     return obj.strip()
            if method == "split":    return obj.split(args[0] if args else " ")
            if method == "contains": return args[0] in obj
            if method == "replace":  return obj.replace(args[0], args[1])
            if method == "length":   return len(obj)

        if isinstance(obj, list):
            if method == "push":     obj.append(args[0]); return None
            if method == "pop":      return obj.pop()
            if method == "length":   return len(obj)
            if method == "get":      return obj[int(args[0])]
            if method == "contains": return args[0] in obj

        if isinstance(obj, UntoldInstance):
            cls = obj.class_def
            for m in cls.methods:
                if m.name == method:
                    local = Environment(parent=env)
                    local.set("self", obj)
                    for i, (pname, _) in enumerate(m.params):
                        local.set(pname, args[i] if i < len(args) else None)
                    try:
                        self.exec_block(m.body, local)
                    except ReturnSignal as r:
                        return r.value
                    return None

        if isinstance(obj, dict):
            if method == "get":    return obj.get(args[0])
            if method == "set":    obj[args[0]] = args[1]; return None
            if method == "keys":   return list(obj.keys())
            if method == "values": return list(obj.values())

        if isinstance(obj, StructInstance):
            if method in obj.fields:
                return obj.fields[method]
            raise AttributeError(f"[Untold] Struct has no field '{method}'")

        raise AttributeError(f"[Untold] No method '{method}' on {type(obj).__name__}")

    def _load_module(self, module, env):
        import os
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

        modules = {
            "untold.fs": "fs",
            "untold.shell": "shell",
            "untold.net": "net",
            "untold.web": "http",
            "untold.ai": "ai",
            "untold.hack": "hack",
            "untold.crypto": "crypto",
        }

        if module in modules:
            try:
                if module == "untold.fs":
                    from stdlib.fs import UntoldFS
                    env.set("fs", UntoldFS)
                elif module == "untold.shell":
                    from stdlib.shell import UntoldShell
                    env.set("shell", UntoldShell)
                elif module == "untold.net":
                    from stdlib.net import UntoldNet
                    env.set("net", UntoldNet)
                elif module == "untold.web":
                    from stdlib.web import UntoldWeb
                    env.set("http", UntoldWeb)
                elif module == "untold.ai":
                    from stdlib.ai import UntoldAI
                    env.set("ai", UntoldAI)
                elif module == "untold.hack":
                    from stdlib.hack import UntoldHack
                    env.set("hack", UntoldHack)
                elif module == "untold.crypto":
                    from stdlib.crypto import UntoldCrypto
                    env.set("crypto", UntoldCrypto)
            except ImportError as e:
                print(f"[Untold] Failed to load module '{module}': {e}")
        else:
            print(f"[Untold] Module '{module}' not found")


class StructInstance:
    def __init__(self, struct_def, fields):
        self.struct_def = struct_def
        self.fields = fields

    def __repr__(self):
        return f"<{self.struct_def.name} {self.fields}>"