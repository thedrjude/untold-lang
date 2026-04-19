from src.lexer.tokens import TokenType

from .ast_nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.type != TokenType.NEWLINE]
        self.pos    = 0

    def current(self):
        return self.tokens[self.pos]

    def peek(self, offset=1):
        p = self.pos + offset
        return self.tokens[p] if p < len(self.tokens) else None

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, ttype, context=""):
        tok = self.current()
        if tok.type != ttype:
            msg = f"[Untold Parser] Expected {ttype}"
            if context:
                msg += f" for {context}"
            msg += f" but got {tok.type} ('{tok.value}') at line {tok.line}"
            raise SyntaxError(msg)
        return self.advance()

    def match(self, *types):
        if self.current().type in types:
            return self.advance()
        return None

    def parse(self):
        stmts = []
        while self.current().type != TokenType.EOF:
            stmts.append(self.parse_statement())
        return Program(stmts)

    def parse_statement(self):
        t = self.current().type

        if t == TokenType.USE:
            return self.parse_use()
        if t == TokenType.START:
            return self.parse_start()
        if t == TokenType.FN or (t == TokenType.ASYNC and
                self.peek() and self.peek().type == TokenType.FN):
            return self.parse_function()
        if t == TokenType.CLASS:
            return self.parse_class()
        if t == TokenType.LET:
            return self.parse_var_decl(constant=False)
        if t == TokenType.LOCK:
            return self.parse_var_decl(constant=True)
        if t == TokenType.RETURN:
            return self.parse_return()
        if t == TokenType.IF:
            return self.parse_if()
        if t == TokenType.LOOP:
            return self.parse_loop()
        if t == TokenType.WHILE:
            return self.parse_while()
        if t == TokenType.TRY:
            return self.parse_try()
        if t == TokenType.BREAK:
            self.advance()
            return BreakStmt()
        if t == TokenType.SKIP:
            self.advance()
            return SkipStmt()

        return self.parse_expr_or_assign()

    def parse_use(self):
        self.expect(TokenType.USE)
        parts = [self.expect(TokenType.IDENTIFIER).value]
        while self.current().type == TokenType.DOT:
            self.advance()
            parts.append(self.expect(TokenType.IDENTIFIER).value)
        return UseStmt(".".join(parts))

    def parse_start(self):
        self.expect(TokenType.START)
        name   = self.expect(TokenType.IDENTIFIER).value
        params = self.parse_params()
        body   = self.parse_block()
        return StartBlock(name, params, body)

    def parse_function(self):
        is_async = False
        if self.current().type == TokenType.ASYNC:
            is_async = True
            self.advance()
        self.expect(TokenType.FN)
        name        = self.expect(TokenType.IDENTIFIER).value
        params      = self.parse_params()
        return_type = None
        if self.current().type == TokenType.ARROW:
            self.advance()
            return_type = self.advance().value
        body = self.parse_block()
        return FunctionDef(name, params, return_type, body, is_async)

    def parse_params(self):
        self.expect(TokenType.LPAREN)
        params = []
        while self.current().type != TokenType.RPAREN:
            name = self.expect(TokenType.IDENTIFIER).value
            type_hint = None
            if self.current().type == TokenType.COLON:
                self.advance()
                type_hint = self.advance().value
            params.append((name, type_hint))
            if self.current().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RPAREN)
        return params

    def parse_class(self):
        self.expect(TokenType.CLASS)
        name    = self.expect(TokenType.IDENTIFIER).value
        fields  = []
        methods = []
        self.expect(TokenType.LBRACE)
        while self.current().type != TokenType.RBRACE:
            if self.current().type in (TokenType.FN, TokenType.ASYNC):
                methods.append(self.parse_function())
            else:
                fname = self.expect(TokenType.IDENTIFIER).value
                self.expect(TokenType.COLON)
                ftype = self.advance().value
                fields.append((fname, ftype))
        self.expect(TokenType.RBRACE)
        return ClassDef(name, fields, methods)

    def parse_var_decl(self, constant):
        self.advance()
        name      = self.expect(TokenType.IDENTIFIER).value
        type_hint = None
        if self.current().type == TokenType.COLON:
            self.advance()
            type_hint = self.advance().value
        self.expect(TokenType.EQ)
        value = self.parse_expr()
        return VarDecl(name, type_hint, value, constant)

    def parse_return(self):
        self.expect(TokenType.RETURN)
        value = self.parse_expr()
        return ReturnStmt(value)

    def parse_if(self):
        self.expect(TokenType.IF)
        condition    = self.parse_expr()
        then_body    = self.parse_block()
        elif_clauses = []
        else_body    = None
        while self.current().type == TokenType.ELIF:
            self.advance()
            ec = self.parse_expr()
            eb = self.parse_block()
            elif_clauses.append((ec, eb))
        if self.current().type == TokenType.ELSE:
            self.advance()
            else_body = self.parse_block()
        return IfStmt(condition, then_body, elif_clauses, else_body)

    def parse_loop(self):
        self.expect(TokenType.LOOP)
        var   = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.IN)
        start = self.parse_primary()
        self.expect(TokenType.DOTDOT)
        end   = self.parse_primary()
        body  = self.parse_block()
        return LoopStmt(var, start, end, body)

    def parse_while(self):
        self.expect(TokenType.WHILE)
        condition = self.parse_expr()
        body      = self.parse_block()
        return WhileStmt(condition, body)

    def parse_try(self):
        self.expect(TokenType.TRY)
        try_body     = self.parse_block()
        catch_var    = None
        catch_body   = None
        finally_body = None
        if self.current().type == TokenType.CATCH:
            self.advance()
            catch_var  = self.expect(TokenType.IDENTIFIER).value
            catch_body = self.parse_block()
        if self.current().type == TokenType.FINALLY:
            self.advance()
            finally_body = self.parse_block()
        return TryCatch(try_body, catch_var, catch_body, finally_body)

    def parse_expr_or_assign(self):
        expr = self.parse_expr()
        if self.current().type == TokenType.EQ:
            if isinstance(expr, Identifier):
                self.advance()
                value = self.parse_expr()
                return AssignStmt(expr.name, value)
        return ExprStmt(expr)

    def parse_block(self):
        self.expect(TokenType.LBRACE)
        stmts = []
        while self.current().type != TokenType.RBRACE:
            stmts.append(self.parse_statement())
        self.expect(TokenType.RBRACE)
        return stmts

    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.current().type == TokenType.OR:
            op   = self.advance().type.name
            left = BinaryOp(left, op, self.parse_and())
        return left

    def parse_and(self):
        left = self.parse_equality()
        while self.current().type == TokenType.AND:
            op   = self.advance().type.name
            left = BinaryOp(left, op, self.parse_equality())
        return left

    def parse_equality(self):
        left = self.parse_comparison()
        while self.current().type in (TokenType.EQEQ, TokenType.NEQ):
            op   = self.advance().type.name
            left = BinaryOp(left, op, self.parse_comparison())
        return left

    def parse_comparison(self):
        left = self.parse_addition()
        while self.current().type in (TokenType.LT, TokenType.GT,
                                      TokenType.LTE, TokenType.GTE):
            op   = self.advance().type.name
            left = BinaryOp(left, op, self.parse_addition())
        return left

    def parse_addition(self):
        left = self.parse_multiplication()
        while self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op   = self.advance().type.name
            left = BinaryOp(left, op, self.parse_multiplication())
        return left

    def parse_multiplication(self):
        left = self.parse_unary()
        while self.current().type in (TokenType.STAR, TokenType.SLASH,
                                      TokenType.PERCENT):
            op   = self.advance().type.name
            left = BinaryOp(left, op, self.parse_unary())
        return left

    def parse_unary(self):
        if self.current().type in (TokenType.NOT, TokenType.MINUS):
            op = self.advance().type.name
            return UnaryOp(op, self.parse_unary())
        return self.parse_call()

    def parse_call(self):
        expr = self.parse_primary()
        while True:
            if self.current().type == TokenType.LPAREN:
                self.advance()
                args = []
                while self.current().type != TokenType.RPAREN:
                    args.append(self.parse_expr())
                    if self.current().type == TokenType.COMMA:
                        self.advance()
                self.expect(TokenType.RPAREN)
                name = expr.name if isinstance(expr, Identifier) else str(expr)
                expr = FunctionCall(name, args)

            elif self.current().type == TokenType.LBRACE and isinstance(expr, Identifier):
                self.advance()
                fields = {}
                while self.current().type != TokenType.RBRACE:
                    key = self.expect(TokenType.IDENTIFIER).value
                    self.expect(TokenType.COLON)
                    val = self.parse_expr()
                    fields[key] = val
                    if self.current().type == TokenType.COMMA:
                        self.advance()
                self.expect(TokenType.RBRACE)
                expr = ClassInstantiation(expr.name, fields)

            elif self.current().type == TokenType.DOT:
                self.advance()
                member = self.expect(TokenType.IDENTIFIER).value
                if self.current().type == TokenType.LPAREN:
                    self.advance()
                    args = []
                    while self.current().type != TokenType.RPAREN:
                        args.append(self.parse_expr())
                        if self.current().type == TokenType.COMMA:
                            self.advance()
                    self.expect(TokenType.RPAREN)
                    expr = MethodCall(expr, member, args)
                else:
                    expr = MemberAccess(expr, member)
            else:
                break
        return expr

    def parse_primary(self):
        tok = self.current()

        if tok.type == TokenType.NUMBER:
            self.advance()
            return NumberLiteral(tok.value)
        if tok.type == TokenType.TEXT:
            self.advance()
            return TextLiteral(tok.value)
        if tok.type in (TokenType.TRUE, TokenType.FALSE):
            self.advance()
            return BoolLiteral(tok.type == TokenType.TRUE)
        if tok.type == TokenType.NULL:
            self.advance()
            return NullLiteral()
        if tok.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(tok.value)
        if tok.type == TokenType.SELF:
            self.advance()
            return Identifier("self")
        if tok.type == TokenType.TYPE_TEXT:
            self.advance()
            return Identifier("text")
        if tok.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expr()
            self.expect(TokenType.RPAREN)
            return expr

        # List literal: [1, 2, 3]
        if tok.type == TokenType.LBRACKET:
            return self.parse_list_literal()

        # Map literal: {"key": value}
        if tok.type == TokenType.LBRACE:
            return self.parse_map_literal()

        raise SyntaxError(
            f"[Untold Parser] Unexpected token {tok.type} "
            f"('{tok.value}') at line {tok.line}"
        )

    def parse_list_literal(self):
        """Parse [expr, expr, ...]"""
        self.advance()  # consume [
        elements = []
        if self.current().type != TokenType.RBRACKET:
            elements.append(self.parse_expr())
            while self.current().type == TokenType.COMMA:
                self.advance()  # consume ,
                elements.append(self.parse_expr())
        self.expect(TokenType.RBRACKET, "list elements")
        return ListLiteral(elements)

    def parse_map_literal(self):
        """Parse {"key": value, ...}"""
        self.advance()  # consume {
        pairs = {}
        if self.current().type != TokenType.RBRACE:
            key = self.expect(TokenType.TEXT, "map key").value
            self.expect(TokenType.COLON, "map key-value separator")
            pairs[key] = self.parse_expr()
            while self.current().type == TokenType.COMMA:
                self.advance()  # consume ,
                key = self.expect(TokenType.TEXT, "map key").value
                self.expect(TokenType.COLON, "map key-value separator")
                pairs[key] = self.parse_expr()
        self.expect(TokenType.RBRACE, "map literal")
        return MapLiteral(pairs)
