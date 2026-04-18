from enum import Enum, auto

class TokenType(Enum):
    # Literals
    NUMBER      = auto()
    TEXT        = auto()
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
    LT          = auto()   # 
    GT          = auto()   # >
    LTE         = auto()   # <=
    GTE         = auto()   # >=
    AND         = auto()   # &&
    OR          = auto()   # ||
    NOT         = auto()   # !
    ARROW       = auto()   # ->
    DOTDOT      = auto()   # ..

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