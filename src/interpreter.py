from math import floor
from typing import Any, Callable, Union

from src.error import RuntimeException, runtime_error
from .expr import Binary, Unary, Visitor, Literal, Expr, Grouping
from .tokens import TokenType, Token


class Interpreter(Visitor):
    def interpret(self, expr: Expr):
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except RuntimeException as e:
            runtime_error(e)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)
    
    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)

        print(expr.operator)
        if expr.operator.token_type is TokenType.MINUS:
            return -float(right)
        elif expr.operator.token_type is TokenType.BANG:
            return not self.is_truthy(right)

        # Should not occur
        print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        return None

    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.token_type is TokenType.PLUS:
            if self.is_num_or_str(left, right):
                if isinstance(left, str) or isinstance(right, str):
                    return self.stringify(left) + self.stringify(right)    
                else:
                    return left + right

            raise RuntimeException("Operators must both be floats or strings.", expr.operator)
        if expr.operator.token_type is TokenType.MINUS:
            self.assert_numbers(expr.operator, left, right)
            return left - right
        elif expr.operator.token_type is TokenType.STAR:
            self.assert_numbers(expr.operator, left, right)
            return left * right
        elif expr.operator.token_type is TokenType.SLASH:
            self.assert_numbers(expr.operator, left, right)
            if right == 0:
                raise RuntimeException("Division by zero error", expr.operator)
            return left / right
        
        else:
            # Expression is a comparison
            left, right = self.num_or_string(left, right)
            gt = lambda x, y: x > y
            lt = lambda x, y: x < y
            eq = lambda x, y: x == y
            geq = lambda x, y: gt(x, y) or eq(x, y)
            leq = lambda x, y: lt(x, y) or eq(x, y)

            def compare(operation: Callable[[Any, Any], bool]):
                if self.is_num_or_string(left, right):
                    return operation(left, right)
                else:
                    raise RuntimeException(f"Comparison {expr.operator.literal} of {left} of type {type(left)} is not possible with {right} of type {type(right)}.", expr.operator)

            if expr.operator.token_type is TokenType.GREATER_EQUAL:
                return compare(geq)
            elif expr.operator.token_type is TokenType.LESS_EQUAL:
                return compare(leq)
            elif expr.operator.token_type is TokenType.GREATER:
                return compare(gt)
            elif expr.operator.token_type is TokenType.LESS:
                return compare(lt)    
            elif expr.operator.token_type is TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

        return None


    def is_truthy(self, value: Any):
        if value is None: return False
        if isinstance(value, bool): return value
        return True

    def is_equal(self, a: Any, b: Any):
        if a is None and b is None: return True
        if a is None: return False
        return a == b

    def assert_numbers(self, operator: Token, *operands):
        for operand in operands:
            if isinstance(operand, float):
                return

        singular = len(operands) == 1
        raise RuntimeException(f"Operand{'' if singular else 's'} must be {'a number' if singular else 'numbers'}.", operator)

    def num_or_string(self, *values: list[Union[int, float]]) -> list[Union[int, float]]:
        if any(isinstance(value, str) for value in values):
            return [str(value) for value in values]
        return values

    def is_num_or_string(self, *values) -> bool:
        return all(isinstance(value, (float, str)) for value in values)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def stringify(self, value: Any) -> str:
        if value is None: return "nil"

        if isinstance(value, float):
            # If the integer representation of a float is the same
            # as the float's rounded value, the float is an integer value.
            i = int(value)
            if i == floor(value):
                return str(i)
            else:
                return str(value)

        return str(value)