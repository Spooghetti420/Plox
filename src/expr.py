from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol
from .tokens import TokenType, Token
from abc import ABC, abstractmethod

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        pass


class Visitor(Protocol):
    def visit_assign_expr(self, expr: Assign):
        pass
    def visit_binary_expr(self, expr: Binary):
        pass
    def visit_call_expr(self, expr: Call):
        pass
    def visit_get_expr(self, expr: Get):
        pass
    def visit_grouping_expr(self, expr: Grouping):
        pass
    def visit_literal_expr(self, expr: Literal):
        pass
    def visit_logical_expr(self, expr: Logical):
        pass
    def visit_set_expr(self, expr: Set):
        pass
    def visit_super_expr(self, expr: Super):
        pass
    def visit_this_expr(self, expr: This):
        pass
    def visit_unary_expr(self, expr: Unary):
        pass
    def visit_variable_expr(self, expr: Variable):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_binary_expr(self)

@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_grouping_expr(self)

@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: Visitor):
        return visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_unary_expr(self)


class ASTPrinter(Visitor):
    def print(self, expression: Expr) -> str:
        return expression.accept(self)

    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)
    
    def visit_literal_expr(self, expr: Literal):
        if expr.value == None: return "nil"
        return str(expr.value)
    
    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *expressions):
        return f"({name} " + " ".join(expr.accept(self) for expr in expressions) + ")"


def main():
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )

    print(ASTPrinter().print(expression))


if __name__ == "__main__":
    main()