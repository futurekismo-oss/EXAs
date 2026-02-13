OPCODES = {"load": 1, "add": 2, "halt": 255, 'print': 10}
REGISTERS = {"r0": 0, "r1": 1}

bytecode = []

with open('test.ac', 'r') as f:
    for line in f:
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
        

pc = 0 # program counter

while pc < len(bytecode):
    instruction = bytecode[pc]
    opcode = instruction[0]
    
    if opcode == 1:
        reg = instruction[1]
        value = instruction[2]
        REGISTERS[reg] = value
    elif opcode == 10:
        reg = instruction[1]
        print(REGISTERS[reg])
    elif opcode == 255:
        break
    
    pc += 1
        
    