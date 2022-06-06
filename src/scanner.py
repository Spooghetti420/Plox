from typing import Any, Optional
from .error import error
from .tokens import Token, TokenType


class Scanner:
    KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self.at_end():
            # We are at the beginning of the next lexeme.
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "!":
            self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif c == "=":
            self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
        elif c == "<":
            self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c == ">":
            self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
        elif c == "/":
            if self.match("*"):
                self.multiline_comment()
            elif self.match("/"):
                while self.peek() != "\n" and not self.at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c.isspace():
            if c == "\n":
                self.line += 1
        elif c == '"':
            self.string()
        elif self.is_decimal_digit(c):
            self.number()
        elif c.isalpha():
            self.identifier()

        else:
            error(self.line, "Unexpected character.")


    def advance(self) -> str:
        self.current += 1
        return self.source[self.current-1]

    def add_token(self, type: TokenType, literal: Optional[Any] = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.at_end(): return False
        if self.source[self.current] != expected: return False
        
        self.current += 1
        return True

    def peek(self) -> str:
        if self.at_end(): return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current+1 >= len(self.source): return "\0"
        return self.source[self.current+1]

    def multiline_comment(self) -> None:
        while not self.at_end():
            c = self.advance()
            if c == "\n":
                self.line += 1
            elif c == "*" and self.peek() == "/":
                self.advance()
                return

    def string(self) -> None:
        while self.peek() != '"' and not self.at_end():
            if self.peek() == "\n": self.line += 1
            self.advance()
        
        if self.at_end():
            error(self.line, "Unterminated string.")
            return
        
        # To capture the closing string quote "
        self.advance()

        self.add_token(TokenType.STRING, self.source[self.start+1:self.current-1])

    def is_decimal_digit(self, char: str) -> bool:
        # No error checking whether char is greater than 1 in length; may implement later.
        return "0" <= char <= "9"

    def number(self) -> None:
        while self.is_decimal_digit(self.peek()): self.advance()

        if self.peek() == "." and self.is_decimal_digit(self.peek_next()):
            # Consume the decimal point
            self.advance()
        
        while self.is_decimal_digit(self.peek()): self.advance()
        
        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self) -> None:
        while self.peek().isalnum(): self.advance()
        text = self.source[self.start:self.current]
        token_type = TokenType.IDENTIFIER if text not in Scanner.KEYWORDS else Scanner.KEYWORDS[text]
        self.add_token(token_type)

    def at_end(self) -> bool:
        return self.current >= len(self.source)


