from typing import Any
from .expr import Visitor, Literal, Expr, Grouping
from tokens import TokenType, Token

class RuntimeException(Exception):
    def __init__(self, message, token: Token):
        super().__init__(message=message)
        self.token = token


class Interpreter(Visitor):
    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)
    
    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)

        self.assert_numbers(expr.operator, expr.right)

        if expr.operator is TokenType.MINUS:
            return -float(right)
        elif expr.operator is TokenType.BANG:
            return not self.is_truthy(right)

        # Should not occur
        return None

    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator is TokenType.PLUS:
            if ((isinstance(left, float) and isinstance(right, float)) or
                isinstance(left, str) and isinstance(right, str)):
                return left + right
            raise RuntimeException(expr.operator, "Operators must both be floats or strings.")
        elif expr.operator is TokenType.MINUS:
            self.assert_numbers(expr.operator, left, right)
            return left - right
        elif expr.operator is TokenType.STAR:
            self.assert_numbers(expr.operator, left, right)
            return left * right
        elif expr.operator is TokenType.SLASH:
            self.assert_numbers(expr.operator, left, right)
            return left / right
        
        elif expr.operator is TokenType.GREATER_EQUAL:
            return float(left) >= float(right)
        elif expr.operator is TokenType.LESS_EQUAL:
            return float(left) <= float(right)
        elif expr.operator is TokenType.GREATER:
            return float(left) > float(right)
        elif expr.operator is TokenType.LESS:
            return float(left) < float(right)
        elif expr.operator is TokenType.EQUAL_EQUAL:
            return left == right

        return None


    def is_truthy(self, value: Any):
        if value is None: return False
        if isinstance(value, bool): return value
        return true

    def is_equal(self, a: Any, b: Any):
        if a is None and b is None: return True
        if a is None: return False
        return a == b

    def assert_numbers(self, operator: Token, *operands: Any):
        for operand in operands:
            if isinstance(operand, float):
                return

        singular = len(operands) == 1
        raise RuntimeException(f"Operand{'' if singular else 's'} must be {'a number' if singular else 'numbers'}.", operator)

    def evaluate(expr: Expr) -> Any:
        return expr.accept(this)