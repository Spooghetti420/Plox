import sys
from src.error import error_occurred
from src.scanner import Scanner
from src.expr import ASTPrinter, Expr
from src.tokens import Token
from src.parser import Parser 


def main(args: list[str]) -> None:
    if len(args) > 1:
        print("Usage: plox [script.lox]")
        sys.exit(64)
    elif len(args) == 1:
        run_file(args[0])
    else:
        run_interpreter()


def run_file(path: str) -> None:
    try:
        with open(path, mode="r", encoding="utf-8") as source_file:
            source = source_file.read()
    except FileNotFoundError:
        print(f"Error: desired file {path} was not found.")
        sys.exit(1)

    run(source)
    if error_occurred():
        sys.exit(65)


def run_interpreter() -> None:
    try:
        while True:
            line = input(">> ")
            run(line)
            error_occurred(False)
    except KeyboardInterrupt:
        return

def run(code: str) -> None:
    scanner = Scanner(code)
    tokens: list[Token] = scanner.scan_tokens()
    parser: Parser = Parser(tokens)
    expression: Expr = parser.parse()

    if error_occurred():
        return

    print(ASTPrinter().print(expression))

if __name__ == "__main__":
    main(sys.argv[1:])