import time
import operator

from utils import execTime, valNum


def exaVm(bytecode: list, register: list) -> str:
    output = ""

    pc = 0  # program counter
    start_time = time.time()
    while pc < len(bytecode):
        instruction = bytecode[pc]
        opcode = instruction[0]

        REG_OPS = {
            2: operator.add,
            3: operator.sub,
            4: operator.mul,
            5: operator.floordiv,
        }

        IMM_OPS = {
            6: operator.add,
            7: operator.sub,
            8: operator.mul,
            9: operator.floordiv,
        }

        if opcode in REG_OPS:
            reg_src1 = valNum(instruction[1], pc)
            reg_src2 = valNum(instruction[2], pc)
            reg_dest = instruction[3]
            register[reg_dest] = REG_OPS[opcode](register[reg_src1], register[reg_src2])

        if opcode in IMM_OPS:
            reg_src1 = valNum(instruction[1], pc)
            value = valNum(instruction[2], pc)
            reg_dest = instruction[3]
            register[reg_dest] = IMM_OPS[opcode](register[reg_src1], value)

        match opcode:
            case 1:
                reg = instruction[1]
                value = instruction[2]
                register[reg] = value
            case 502:  # sload
                reg = instruction[1]
                string = instruction[2]
                register[reg] = string
            case 11:  # copy
                reg_src = instruction[1]
                reg_dest = instruction[2]
                register[reg_dest] = register[reg_src]
            case 10:  # print
                reg = instruction[1]

                for item in instruction[1:]:
                    if isinstance(item, str):
                        output += str(item) + " "
                    else:
                        output += str(register[item]) + " "
            case 500:  # input
                reg = instruction[1]
                mode = instruction[2]
                text = instruction[3]

                user_input = input(text)

                if mode == 1:
                    # Store as string
                    register[reg] = user_input
                else:
                    # try to store as a int, fallback to string
                    try:
                        register[reg] = int(user_input)
                    except ValueError:
                        register[reg] = user_input
            case 501:  # concat
                reg_src1 = instruction[1]
                reg_src2 = instruction[2]
                reg_dest = instruction[3]

                register[reg_dest] = str(register[reg_src1]) + str(register[reg_src2])
            case 404:  # jump
                pc = instruction[1]
                continue
            case 406:  # jumpr
                reg = register[instruction[2]]
                mode = instruction[3]

                if mode == 1:
                    if reg == 0:
                        pc = instruction[1]
                        continue
                else:
                    if reg != 0:
                        pc = instruction[1]
                        continue

            case 255:
                end_time = time.time()
                execTime(end_time - start_time, "halt")
                break
            case 256:
                end_time = time.time()
                execTime(end_time - start_time, "kill")
                break
            case 503:
                output += "\n"

        pc += 1
    return output
