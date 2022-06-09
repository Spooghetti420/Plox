from typing import Union
from .tokens import Token, TokenType
from .expr import Expr, Binary, Literal, Unary, Grouping
from .error import error

class ParseError(Exception):
    pass

class Parser:
    """
    A recursive decent parser, which takes in a flat list of tokens generated
    by a lexer, converting them into a semantically gravid structure.
    """
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current: int = 0

    def parse(self) -> Union[Expr, None]:
        try:
            return self.expression()
        except ParseError:
            return

    # The below methods implement a context-free grammar, with this hierarchy:
    # (higher-up terms have lower precedence, so they expand to contain other terms)
    """ expression     → equality ;
        equality       → comparison ( ( "!=" | "==" ) comparison )* ;
        comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        term           → factor ( ( "-" | "+" ) factor )* ;
        factor         → unary ( ( "/" | "*" ) unary )* ;
        unary          → ( "!" | "-" ) unary
                    | primary ;
        primary        → NUMBER | STRING | "true" | "false" | "nil"
                    | "(" expression ")" ;
    """

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr: Expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)

        return expr


    def term(self) -> Expr:
        expr: Expr = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr: Expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: Expr = self.unary()
            return Unary(operator, right)
        
        return self.primary()
    
    def primary(self) -> Expr:
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)
        
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after '(' expression.")
            return Grouping(expr)

        self.error(self.peek(), "Expected expression.")


    def match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        
        return False

    def check(self, token_type: TokenType) -> bool:
        if self.at_end(): return False
        return self.peek().token_type is token_type

    def advance(self):
        if not self.at_end():
            self.current += 1
        return self.previous()

    def at_end(self) -> bool:
        return self.peek().token_type is TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]

    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type): return self.advance()
        self.error(self.peek(), message)

    def report(self, line, message) -> ParseError:
        error(line, message)
        return ParseError()

    def error(self, token: Token, message: str) -> None:
        if token.token_type is TokenType.EOF:
            self.report(token.line, f"at end {message}")
        else:
            self.report(token.line, f"at '{token.lexeme}' {message}")

    def synchronize(self) -> None:
        """
        Discard tokens until a statement-delimiting token type is found.
        """
        self.advance()

        while not self.at_end():
            if self.previous().token_type is TokenType.SEMICOLON:
                return
            
            t = self.peek().token_type
            if t in (
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN
            ): return
        
            self.advance()