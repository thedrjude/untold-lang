from .tokens import Token, TokenType

KEYWORDS = {
    "start"  : TokenType.START,
    "fn"     : TokenType.FN,
    "async"  : TokenType.ASYNC,
    "wait"   : TokenType.WAIT,
    "let"    : TokenType.LET,
    "lock"   : TokenType.LOCK,
    "return" : TokenType.RETURN,
    "if"     : TokenType.IF,
    "elif"   : TokenType.ELIF,
    "else"   : TokenType.ELSE,
    "loop"   : TokenType.LOOP,
    "while"  : TokenType.WHILE,
    "in"     : TokenType.IN,
    "break"  : TokenType.BREAK,
    "skip"   : TokenType.SKIP,
    "class"  : TokenType.CLASS,
    "self"   : TokenType.SELF,
    "use"    : TokenType.USE,
    "try"    : TokenType.TRY,
    "catch"  : TokenType.CATCH,
    "finally": TokenType.FINALLY,
    "true"   : TokenType.TRUE,
    "false"  : TokenType.FALSE,
    "null"   : TokenType.NULL,
    "num"    : TokenType.TYPE_NUM,
    "bool"   : TokenType.TYPE_BOOL,
    "list"   : TokenType.TYPE_LIST,
    "map"    : TokenType.TYPE_MAP,
    "void"   : TokenType.TYPE_VOID,
    "any"    : TokenType.TYPE_ANY,
}

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos    = 0
        self.line   = 1
        self.tokens = []

    def current(self):
        return self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self, offset=1):
        p = self.pos + offset
        return self.source[p] if p < len(self.source) else None

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
        return ch

    def add(self, type, value=None):
        self.tokens.append(Token(type, value, self.line))

    def tokenize(self):
        while self.pos < len(self.source):
            ch = self.current()

            # Whitespace (ignore spaces/tabs)
            if ch in (" ", "\t", "\r"):
                self.advance()

            # Newline
            elif ch == "\n":
                self.add(TokenType.NEWLINE)
                self.advance()

            # Single-line comment
            elif ch == "/" and self.peek() == "/":
                while self.current() and self.current() != "\n":
                    self.advance()

            # Multi-line comment
            elif ch == "/" and self.peek() == "*":
                self.advance(); self.advance()
                while self.current():
                    if self.current() == "*" and self.peek() == "/":
                        self.advance(); self.advance()
                        break
                    self.advance()

            # String literal
            elif ch == '"':
                self.advance()
                result = ""
                while self.current() and self.current() != '"':
                    result += self.advance()
                self.advance()
                self.add(TokenType.TEXT, result)

            # Number
            # Number
            elif ch.isdigit():
                num = ""
                while self.current() and self.current().isdigit():
                    num += self.advance()
                # Only consume a dot if it's a decimal (next char is a digit, not another dot)
                if self.current() == "." and self.peek() and self.peek() != "." and self.peek().isdigit():
                    num += self.advance()  # consume the dot
                    while self.current() and self.current().isdigit():
                        num += self.advance()
                    self.add(TokenType.NUMBER, float(num))
                else:
                    self.add(TokenType.NUMBER, int(num))

            # Identifier or keyword
            elif ch.isalpha() or ch == "_":
                word = ""
                while self.current() and (self.current().isalnum() or self.current() == "_"):
                    word += self.advance()
                ttype = KEYWORDS.get(word, TokenType.IDENTIFIER)
                self.add(ttype, word)

            # Two-char operators
            elif ch == "-" and self.peek() == ">":
                self.advance(); self.advance()
                self.add(TokenType.ARROW)
            elif ch == "." and self.peek() == ".":
                self.advance(); self.advance()
                self.add(TokenType.DOTDOT)
            elif ch == "=" and self.peek() == "=":
                self.advance(); self.advance()
                self.add(TokenType.EQEQ)
            elif ch == "!" and self.peek() == "=":
                self.advance(); self.advance()
                self.add(TokenType.NEQ)
            elif ch == "<" and self.peek() == "=":
                self.advance(); self.advance()
                self.add(TokenType.LTE)
            elif ch == ">" and self.peek() == "=":
                self.advance(); self.advance()
                self.add(TokenType.GTE)
            elif ch == "&" and self.peek() == "&":
                self.advance(); self.advance()
                self.add(TokenType.AND)
            elif ch == "|" and self.peek() == "|":
                self.advance(); self.advance()
                self.add(TokenType.OR)

            # Single-char operators & delimiters
            else:
                single = {
                    "+": TokenType.PLUS,   "-": TokenType.MINUS,
                    "*": TokenType.STAR,   "/": TokenType.SLASH,
                    "%": TokenType.PERCENT,"=": TokenType.EQ,
                    "<": TokenType.LT,     ">": TokenType.GT,
                    "!": TokenType.NOT,    "(": TokenType.LPAREN,
                    ")": TokenType.RPAREN, "{": TokenType.LBRACE,
                    "}": TokenType.RBRACE, "[": TokenType.LBRACKET,
                    "]": TokenType.RBRACKET,",": TokenType.COMMA,
                    ".": TokenType.DOT,    ":": TokenType.COLON,
                }
                if ch in single:
                    self.advance()
                    self.add(single[ch])
                else:
                    raise SyntaxError(f"[Untold Lexer] Unknown character '{ch}' at line {self.line}")

        self.add(TokenType.EOF)
        return self.tokens