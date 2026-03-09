# pyright: reportMissingImports=false
import sys
from compiler import Compiler
from vm import exaVm


def validate_file():
    if len(sys.argv) < 2:
        print("Usage: python3 exa.py <file.ac>")
        sys.exit(1)

    source = sys.argv[1]

    if not source.endswith(".ac"):
        print("Error: File must be a .ac file")
        sys.exit(1)

    return source


debug_mode = "--debug" in sys.argv
filename = validate_file()
compiler = Compiler()
bytecode = compiler.compile(filename, debug=debug_mode)

# After assembler builds REG dict:
register: list[int | str] = [0] * compiler.register_count  # Create enough registers

if __name__ == "__main__":
    print(exaVm(bytecode, register))
