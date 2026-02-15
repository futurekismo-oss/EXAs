# EXA TODO

## Phase 1: Core Interactivity (PRIORITY)
- [ ] **input instruction** - `input <register> <mode>`
  - Mode 0: try convert to int, fallback to string
  - Mode 1: force store as string
  - Update `data.json` with opcode and argument count
  - Implement VM case for reading stdin
  - Change `register` initialization to `[None] * register_count` to support any type

## Phase 2: String Comparison
- [ ] **scmp** - `scmp <location> <reg1> <reg2> <mode>` (string compare + jump)
  - Mode 0: jump if equal
  - Mode 1: jump if not equal
  
- [ ] **scmpt** - `scmpt <reg1> <reg2> <result_reg> <mode>` (string compare + store result)
  - Mode 0: store 1 if equal, 0 if not
  - Mode 1: store 1 if not equal, 0 if equal

## Phase 3: Numeric Comparison
- [ ] **jumpc** - `jumpc <location> <reg1> <reg2> <mode>` (numeric compare + jump)
  - Mode 0: jump if equal
  - Mode 1: jump if not equal
  - Mode 2: jump if reg1 > reg2
  - Mode 3: jump if reg1 < reg2
  - Mode 4: jump if reg1 >= reg2
  - Mode 5: jump if reg1 <= reg2

- [ ] **jumpcr** - `jumpcr <reg1> <reg2> <result_reg> <mode>` (numeric compare + store result)
  - Same modes as jumpc, stores 1 if true, 0 if false

## Phase 4: File I/O (Makes EXA Actually Useful)
- [ ] **fread** - `fread <filename_reg> <content_reg>` (read entire file into register)
- [ ] **fwrite** - `fwrite <filename_reg> <content_reg>` (write register content to file)
- [ ] **fappend** - `fappend <filename_reg> <content_reg>` (append to file)

## Phase 5: String Operations
- [ ] **concat** - `concat <reg1> <reg2> <result_reg>` (concatenate two strings)
- [ ] **strlen** - `strlen <reg> <result_reg>` (get string length)
- [ ] **substr** - `substr <reg> <start> <length> <result_reg>` (get substring)

## Phase 6: Advanced Features (Future)
- [ ] **call/ret** - Function calls with return addresses
- [ ] **push/pop** - Stack operations
- [ ] **and/or/xor/not** - Bitwise operations
- [ ] **shl/shr** - Bit shifts
- [ ] **malloc/free** - Dynamic memory (if moving away from auto-registers)

## Infrastructure Improvements
- [ ] **Variable argument system** - Only implement if 4+ instructions need it
  - Add `variable_args` section to `data.json`
  - Format: `"instruction": [min_args, max_args]`
  - Update validation logic to check this first
  
- [ ] **Better error messages** - Show actual line content in errors, not just line number

- [ ] **Debugger mode** - Step through execution, inspect registers

- [ ] **REPL mode** - Interactive EXA shell for quick testing

## Testing Milestones
- [ ] **Milestone 1**: Write program that asks for name, prints greeting
- [ ] **Milestone 2**: Write program that reads file, processes it, writes output
- [ ] **Milestone 3**: Write interactive calculator with string/number handling
- [ ] **Milestone 4**: Write text adventure game (tests all features)

## Documentation
- [ ] Update README.md with new instructions as they're added
- [ ] Add examples folder with sample programs
- [ ] Create SYNTAX.md with complete language reference

---

**Notes:**
- Keep the "unsafe but powerful" philosophy - let users shoot themselves in the foot
- Flexibility over safety (registers hold any type)
- Complete Phase 1-3 before considering C port
- Only build variable args system if actually needed for 4+ instructions
