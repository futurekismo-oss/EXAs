# EXA

A lightweight, assembly-like programming language with its own compiler and virtual machine.

## Installation

```bash
git clone <repository-url>
cd EXAs
```

## Quick Start

```bash
# Run a program
python3 src/exa.py program.ac

# Run with debug mode (shows bytecode)
python3 src/exa.py program.ac --debug
```

## Example

```exa
print "Hello, World!"
halt
```

Save as `hello.ac` and run with `python3 src/exa.py hello.ac`.

## Documentation

See [DOCUMENTATION.md](DOCUMENTATION.md) for the full language specification.

## Project Structure

| File | Description |
|------|-------------|
| `src/exa.py` | Entry point and CLI |
| `src/compiler.py` | Source code to bytecode compiler |
| `src/vm.py` | Virtual machine executor |
| `src/settings.py` | Configuration and opcodes |
| `src/utils.py` | Utility functions |
| `data/data.json` | Opcode definitions and colors |
| `extras/mini_projects/` | Example programs |

## License

2026, Futurekismo
