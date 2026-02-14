import sys
import time
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Hashmaps, located in json files

with open(os.path.join(BASE_DIR, "data.json"), "r") as data:
    data = json.load(data)

    OPCODES = data["opcodes"]
    COLORS = data["terminal_colors"]
    # REG = data["registers"]

REG = {}
register_count = 0
r, g, b, y, reset = (
    COLORS["red"],
    COLORS["green"],
    COLORS["blue"],
    COLORS["yellow"],
    COLORS["reset"],
)


def print_execution_time(exec_time, mode):
    exec_time_ms = exec_time * 1000
    
    if mode == "halt":
        print(f"{g}Execution state: {b}finished{reset}, {y}{exec_time_ms:.2f}ms{reset}")
    elif mode == "kill":
        print(f"{g}Execution state: {r}CANCELLED{reset}, {y}{exec_time_ms:.2f}ms{reset}")


def error(message, pc):
    print(f"{r}ERROR: {message}.{reset}")
    pc += 1 #make it actual line rather than the index line
    print(f"{y}line: {pc} ({filename}){reset}")
    
def generate_bytcode():
    if not debug_mode:
        return
    
    bytename = filename.rsplit('.', 1)[0] + ".acb"
    
    with open(bytename, 'w') as bytefile:
        json.dump(bytecode, bytefile)
        
    print(f"{y}Debug: Bytecode saved to {bytename}{reset}")

bytecode = []

if len(sys.argv) < 2:
    print("Usage: python3 exa.py <file.ac>")
    sys.exit(1)

filename = sys.argv[1]
debug_mode = "--debug" in sys.argv

if not filename.endswith(".ac"):
    print("Error: File must be a .ac file")
    sys.exit(1)
    
LABELS = {}
lines = []
instruction_index = 0


with open(filename, "r") as f:
    for raw_line in f:

        if "<<" in raw_line:
            raw_line = raw_line.split("<<")[0]

        line = raw_line.strip()
        if not line:
            continue

        # Label (do NOT count as instruction)
        if line.endswith(":"):
            label_name = line[:-1].lower()
            LABELS[label_name] = instruction_index
            continue

        # Real instruction
        lines.append(line)
        instruction_index += 1
        
    for line in lines:
        instruction_bytes = []
        if '"' in line:
            # split the string
            before_quote = line.split('"')[0].strip()
            string_content = line.split('"')[1]

            # Get instructions
            parts = before_quote.split()
            instruction = parts[0].lower()
            instruction_bytes.append(OPCODES[instruction])

            # Add any args before the string
            for i in range(1, len(parts)):
                arg = parts[i].lower()

                # Is it a label reference?
                if arg in LABELS:
                    instruction_bytes.append(LABELS[arg])

                # Is it a register?
                elif arg.isalpha():
                    # If this instruction expects a label but didn't find one,
                    # treat as register ONLY if it's not used in a jump.
                    if instruction in ["jump", "jumpz"] and arg not in REG:
                        print(f"Error: Undefined label '{arg}'")
                        sys.exit(1)

                    if arg not in REG:
                        REG[arg] = register_count
                        register_count += 1
                    instruction_bytes.append(REG[arg])
                else:
                    instruction_bytes.append(int(arg))

            # Add the string itself
            instruction_bytes.append(string_content)

        else:
            # Normal instruction (no string)
            parts = line.split()
            instruction = parts[0].lower()
            instruction_bytes.append(OPCODES[instruction])

            for i in range(1, len(parts)):
                arg = parts[i].lower()

                # Is it a label reference?
                if arg in LABELS:
                    instruction_bytes.append(LABELS[arg])

                # Is it a register?
                                
                elif arg.isalpha():
                    # If this instruction expects a label but didn't find one,
                    # treat as register ONLY if it's not used in a jump.
                    if instruction in ["jump", "jumpz"] and arg not in REG:
                        print(f"Error: Undefined label '{arg}'")
                        sys.exit(1)

                    if arg not in REG:
                        REG[arg] = register_count
                        register_count += 1
                    instruction_bytes.append(REG[arg])
                else:  # Then its a number
                    instruction_bytes.append(int(arg))

        bytecode.append(instruction_bytes)
        
generate_bytcode()

# After assembler builds REG dict:
register = [0] * register_count  # Create enough registers

pc = 0  # program counter
start_time = time.time()
while pc < len(bytecode):

    instruction = bytecode[pc]
    opcode = instruction[0]

    match opcode:
        case 1:
            value = instruction[1]
            reg = instruction[2]
            register[reg] = value
            
            
        case 2:  # add
            reg_src1 = instruction[1]
            reg_src2 = instruction[2]
            reg_dest = instruction[3]
            register[reg_dest] = register[reg_src1] + register[reg_src2]
        case 3:  # sub
            reg_src1 = instruction[1]
            reg_src2 = instruction[2]
            reg_dest = instruction[3]
            register[reg_dest] = register[reg_src1] - register[reg_src2]
        case 4:  # muli
            reg_src1 = instruction[1]
            reg_src2 = instruction[2]
            reg_dest = instruction[3]
            register[reg_dest] = register[reg_src1] * register[reg_src2]
        case 5:  # div
            reg_src1 = instruction[1]
            reg_src2 = instruction[2]
            
            if register[reg_src2] == 0:
                error("You cannot divide by zero", pc)
                break
            
            reg_dest = instruction[3]
            register[reg_dest] = register[reg_src1] // register[reg_src2]
            
        case 6: #addi
            reg_src = instruction[1]
            value = instruction[2]
            reg_dest = instruction[3]
            register[reg_dest] = register[reg_src] + value
        case 7: #subi
            reg_src = instruction[1]
            value = instruction[2]
            reg_dest = instruction[3]
            register[reg_dest] = register[reg_src] - value
        case 8: #mulii
            reg_src = instruction[1]
            value = instruction[2]
            reg_dest = instruction[3]
            register[reg_dest] = register[reg_src] * value
        case 9: #divi
            reg_src = instruction[1]
            value = instruction[2]
            
            if value == 0:
                error("You cannot divide by 0", pc)
                break
            
            reg_dest = instruction[3]
            register[reg_dest] = register[reg_src] // value
        
        case 11: #copy
            reg_src = instruction[1]
            reg_dest = instruction[2]

            register[reg_dest] = register[reg_src]
        
        case 10:  # print
            reg = instruction[1]

            if isinstance(reg, str):
                print(reg)
            else:
                print(register[reg])
                
                
        case 404:  # jump
            pc = instruction[1]
            continue
        case 406:  # jumpz
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
            print_execution_time(end_time - start_time, "halt")
            break
        case 256:
            end_time = time.time()
            print_execution_time(end_time - start_time, "kill")
            break

    pc += 1
