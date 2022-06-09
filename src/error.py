from traceback import print_tb
from src.tokens import Token

class RuntimeException(Exception):
    def __init__(self, message, token: Token):
        super().__init__()
        self.message = message
        self.token = token

_error_occurred = False
_runtime_error_occurred = False
def error(line: int, message: str) -> None:
    global _error_occurred
    _error_occurred = True
    print(f"Error on line {line}: {message}")

def error_occurred(error: bool = None):
    global _error_occurred
    if type(error) is bool:
        _error_occurred = error

    return _error_occurred

def runtime_error(error: RuntimeException):
    print(
        f"{error.message} [Line {error.token.line}]"
    )
    runtime_error_occurred(True)

def runtime_error_occurred(error: bool = None):
    global _runtime_error_occurred
    if type(error) is bool:
        _runtime_error_occurred = error
    
    return _runtime_error_occurred