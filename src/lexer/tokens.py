from enum import Enum, auto


class TokenType(Enum):
    # Literals
    NUMBER      = auto()
    TEXT        = auto()
    TEXT_TEMPLATE = auto()  # `Hello ${name}`
    BOOL        = auto()
    NULL        = auto()
    IDENTIFIER  = auto()

    # Keywords
    START       = auto()
    FN          = auto()
    ASYNC       = auto()
    WAIT        = auto()
    LET         = auto()
    LOCK        = auto()
    RETURN      = auto()
    IF          = auto()
    ELIF        = auto()
    ELSE        = auto()
    LOOP        = auto()
    WHILE       = auto()
    IN          = auto()
    BREAK       = auto()
    SKIP        = auto()
    CLASS       = auto()
    SELF        = auto()
    USE         = auto()
    TRY         = auto()
    CATCH       = auto()
    FINALLY     = auto()
    TRUE        = auto()
    FALSE       = auto()
    ENUM        = auto()    # enum Status { ... }
    STRUCT      = auto()    # struct Point { ... }
    TEST        = auto()    # test "name" { ... }
    ASSERT      = auto()    # assert(condition)
    ASSERT_EQ   = auto()    # assert_eq(a, b)
    MATCH       = auto()    # match value { ... }
    ELSE_MATCH  = auto()    # else -> in match
    THROW       = auto()    # throw Error{ ... }
    YIELD       = auto()    # yield value

    # Decorator
    AT          = auto()    # @decorator

    # Try expression
    ELVIS       = auto()    # ?? fallback operator

    # Types
    TYPE_NUM    = auto()
    TYPE_TEXT   = auto()
    TYPE_BOOL   = auto()
    TYPE_LIST   = auto()
    TYPE_MAP    = auto()
    TYPE_VOID   = auto()
    TYPE_ANY    = auto()

    # Operators
    PLUS        = auto()
    MINUS       = auto()
    STAR        = auto()
    SLASH       = auto()
    PERCENT     = auto()
    EQ          = auto()   # =
    EQEQ        = auto()   # ==
    NEQ         = auto()   # !=
    LT          = auto()   # <
    GT          = auto()   # >
    LTE         = auto()   # <=
    GTE         = auto()   # >=
    AND         = auto()   # &&
    OR          = auto()   # ||
    NOT         = auto()   # !
    ARROW       = auto()   # ->
    DOTDOT      = auto()   # ..
    DOTDOTDOT   = auto()   # ... for list comprehension

    # Delimiters
    LPAREN      = auto()   # (
    RPAREN      = auto()   # )
    LBRACE      = auto()   # {
    RBRACE      = auto()   # }
    LBRACKET    = auto()   # [
    RBRACKET    = auto()   # ]
    COMMA       = auto()
    DOT         = auto()
    COLON       = auto()
    NEWLINE     = auto()

    # Special
    EOF         = auto()
    COMMENT     = auto()

class Token:
    def __init__(self, type: TokenType, value, line: int):
        self.type  = type
        self.value = value
        self.line  = line

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line})"