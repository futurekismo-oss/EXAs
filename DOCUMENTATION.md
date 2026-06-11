# EXA

A lightweight, assembly-like programming language with its own compiler and virtual machine.

- **Basic or Assembly-like syntax**
- **Built on Python3**
- **File extension:** `.ac`

---

## Quick Start

```bash
# Run a program
python3 src/exa.py program.ac

# Run with bytecode debug output
python3 src/exa.py program.ac --debug
```

---

## Documentation

### TERMS

**OPCODES** are built-in instructions/functions in EXA.

**REGISTERS** are variables that hold values (e.g., `x`, `box`).

**VALUES** are base-10 numbers.

**LABELS** mark locations for jumps (e.g., `loop:`, `start:`).

---

### OPCODES

#### Data Operations

- **`load`**: Load a value into a register
  ```
  load <register> <value>
  load x 42        << x = 42
  ```

- **`sload`**: Load a string into a register
  ```
  sload <register> "<string>"
  sload name "Alice"  << name = "Alice"
  ```

- **`copy`**: Copy a register's value to another register
  ```
  copy <src_register> <dest_register>
  copy x y           << y = x
  ```

- **`concat`**: Concatenate two registers and store in another
  ```
  concat <register1> <register2> <dest_register>
  concat first last fullname  << fullname = first + last
  ```

#### Input/Output

- **`print`**: Print a string or register value
  ```
  print <string / register>
  print "Hello"      << prints Hello
  print x            << prints value of x
  ```

- **`input`**: Get user input (mode 1 = string, mode 2 = int or string fallback)
  ```
  input <register> <mode> <prompt>
  input name "Name: " 1
  input age "Age: " 2


- **`nl`**: Use nl to print a newline
  ```
  nl << prints a newline thats its
  ```

#### Arithmetic (Register-based)

Requires all three registers to be pre-defined with `load`.

- **`add`**: Add two registers
  ```
  add <register1> <register2> <dest_register>
  add x y z          << z = x + y
  ```

- **`sub`**: Subtract two registers
  ```
  sub <register1> <register2> <dest_register>
  sub x y z          << z = x - y
  ```

- **`mul`**: Multiply two registers
  ```
  mul <register1> <register2> <dest_register>
  mul x y z          << z = x * y
  ```

- **`div`**: Divide two registers (integer division)
  ```
  div <register1> <register2> <dest_register>
  div x y z          << z = x / y (floor)
  ```

#### Arithmetic (Immediate)

Performs arithmetic with a register and a constant value.

- **`addi`**: Add immediate value
  ```
  addi <register> <value> <dest_register>
  addi x 1 z         << z = x + 1
  ```

- **`subi`**: Subtract immediate value
  ```
  subi <register> <value> <dest_register>
  subi x 5 z         << z = x - 5
  ```

- **`mulii`**: Multiply by immediate value
  ```
  mulii <register> <value> <dest_register>
  mulii x 2 z        << z = x * 2
  ```

- **`divi`**: Divide by immediate value
  ```
  divi <register> <value> <dest_register>
  divi x 2 z         << z = x / 2 (floor)
  ```

#### Control Flow

- **`jump`**: Unconditional jump to a label
  ```
  jump <label>
  jump loop          << go to 'loop:'
  ```

- **`jumpz`**: Conditional jump based on register value
  ```
  jumpz <label> <register> <mode>
  jumpz end counter 0    << jump if counter != 0 (mode 0)
  jumpz end counter 1     << jump if counter == 0 (mode 1)
  ```

- **`jumpr`**: Reverse conditional jump (opposite logic)
  ```
  jumpr <label> <register> <mode>
  jumpr skip value 0      << jump if value == 0 (mode 0)
  jumpr skip value 1      << jump if value != 0 (mode 1)
  ```

#### Execution Control

- **`halt`**: End program successfully, print execution time
  ```
  halt
  ```

- **`kill`**: End program with failure status, print execution time
  ```
  kill
  ```

---

### COMMENTS

Use `<<` to add comments:

```
print x << this is a comment
<< this is a standalone comment
```

---

### EXAMPLES

#### Hello World
```
print "hello world"
```

#### Simple Calculator
```
load x 10
load y 5
add x y z
print z           << prints 15
halt
```

#### Loop
```
load counter 3
load one 1
loop:
print counter
subi counter 1 counter
jumpz end counter 0
jump loop
end:
print "done"
halt
```

#### String Concatenation
```
sload first "Hello "
sload second "World"
concat first second message
print message        << prints "Hello World"
halt
```

---

### HOW TO RUN

```bash
python3 src/exa.py <your_program>.ac
python3 src/exa.py <your_program>.ac --debug  << shows bytecode
```

---

## Project Structure

```
EXAs/
├── src/
│   ├── exa.py       << Entry point
│   ├── compiler.py  << Source -> bytecode
│   ├── vm.py        << Bytecode executor
│   ├── settings.py  << Configuration
│   └── utils.py     << Helpers
├── data/
│   └── data.json    << Opcodes & colors
├── extras/
│   └── mini_projects/  << Example programs
└── DOCUMENTATION.md
```

---

###### 2026, Futurekismo
