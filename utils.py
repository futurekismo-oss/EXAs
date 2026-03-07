from settings import color  # type: ignore
import sys
import json


def exec_time(exec_time, mode):
    exec_time_ms = exec_time * 1000

    if mode == "halt":
        print(
            f"{color.g}Execution state: {color.b}finished{color.reset}, {color.y}{exec_time_ms:.2f}ms{color.reset}"
        )
    elif mode == "kill":
        print(
            f"{color.g}Execution state: {color.r}CANCELLED{color.reset}, {color.y}{exec_time_ms:.2f}ms{color.reset}"
        )


def error(message, pc):
    print(f"{color.r}ERROR: {message}.{color.reset}")
    pc += 1  # make it actual line rather than the index line
    print(f"{color.y}line: {pc} {color.reset}")
    sys.exit(1)


def gen_bytecode(filename, bytecode):
    bytename = filename.rsplit(".", 1)[0] + ".acb"

    with open(bytename, "w") as bytefile:
        json.dump(bytecode, bytefile)

    print(f"{color.y}Debug: Bytecode saved to {bytename}{color.reset}")
