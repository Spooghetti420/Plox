import sys

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


def run_interpreter() -> None:
    try:
        while True:
            line = input(">> ")
            run(line)
    except KeyboardInterrupt:
        return


def run(code: str) -> None:
    pass


if __name__ == "__main__":
    main(sys.argv[1:])