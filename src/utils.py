from settings import color  # type: ignore
import sys
import json


def execTime(exec_time, mode):
    exec_time_ms = exec_time * 1000

    if mode == "halt":
        print(
            f"{color['g']}Execution state: {color['b']}finished{color['r']}, {color['y']}{exec_time_ms:.2f}ms{color['r']}"
        )
    elif mode == "kill":
        print(
            f"{color['g']}Execution state: {color['r']}CANCELLED{color['r']}, {color['y']}{exec_time_ms:.2f}ms{color['r']}"
        )


def error(message, pc):
    print(f"{color['r']}ERROR: {message}.{color['r']}")
    pc += 1  # make it actual line rather than the index line
    print(f"{color['y']}line: {pc} {color['r']}")
    sys.exit(1)


def genBytecode(filename, bytecode):
    bytename = filename.rsplit(".", 1)[0] + ".acb"

    with open(bytename, "w") as bytefile:
        json.dump(bytecode, bytefile)

    print(f"{color['y']}Debug: Bytecode saved to {bytename}{color['r']}")


def valNum(number, pc):
    if not isinstance(number, int):
        error("You can only perform arithemic operation on integers", pc)

    return number
