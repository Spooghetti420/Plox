_error_occurred = False
def error(line: int, message: str) -> None:
    global _error_occurred
    _error_occurred = True
    print(f"Error on line {line}: {message}")

def error_occurred(error: bool = None):
    global _error_occurred
    if type(error) is bool:
        _error_occurred = error

    return _error_occurred