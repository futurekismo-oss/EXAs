import sys
import time
import json

# Hashmaps, located in json files

with open("json's/OPCODES.json", "r") as opcodes:
    OPCODES = json.load(opcodes)
    
with open("json's/REGISTER.json", "r") as registers:
    REGISTERS = json.load(registers)
    
with open("json's/TERMINAL_COLORS.json", "r") as colors:
    TERMINAL_COLORS = json.load(colors)




def print_execution_time(exec_time):
    exec_time_ms = exec_time * 1000
    g, b, y, r = (
        TERMINAL_COLORS["green"],
        TERMINAL_COLORS["blue"],
        TERMINAL_COLORS["yellow"],
        TERMINAL_COLORS["reset"],
    )
    print(f"{g}Execution state: {b}finished{r}, {y}{exec_time_ms:.2f}ms{r}")


bytecode = []
register = [0, 0]

start_time = time.time()

if len(sys.argv) < 2:
    print("Usage: python3 exa.py <file.ac>")
    sys.exit(1)

filename = sys.argv[1]

if not filename.endswith(".ac"):
    print("Error: File must be a .ac file")
    sys.exit(1)

with open(filename, "r") as f:
    for line in f:
        # Remove comments
        if "<<" in line:
            line = line.split("<<")[0]

        parts = line.strip().split()

        if not parts:
            continue

        instruction_bytes = []

        instruction = parts[0].lower()
        instruction_bytes.append(OPCODES[instruction])

        for i in range(1, len(parts)):
            arg = parts[i].lower()

            if arg in REGISTERS:
                instruction_bytes.append(REGISTERS[arg])
            else:
                instruction_bytes.append(int(arg))

        bytecode.append(instruction_bytes)

with open("test.ach", "w") as f:
    f.write(str(bytecode))

pc = 0  # program counter

while pc < len(bytecode):

    if arg in REGISTERS:
        instruction_bytes.append(REGISTERS[arg])

    instruction = bytecode[pc]
    opcode = instruction[0]

    if opcode == 1:
        value = instruction[1]
        reg = instruction[2]
        register[reg] = value
    if opcode == 2:
        reg_src1 = instruction[1]
        reg_src2 = instruction[2]
        reg_dest = instruction[3]

        register[reg_dest] = register[reg_src1] + register[reg_src2]

    elif opcode == 3:
        reg_src1 = instruction[1]
        reg_src2 = instruction[2]
        reg_dest = instruction[3]

        register[reg_dest] = register[reg_src1] - register[reg_src2]

    elif opcode == 10:
        reg = instruction[1]
        print(register[reg])
    elif opcode == 255:
        end_time = time.time()
        print_execution_time(end_time - start_time)
        break

    pc += 1
