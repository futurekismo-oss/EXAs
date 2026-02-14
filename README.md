# **EXAs**
my programming language comes with compiler and assembler
Basic or Assemblg-like.

# **Documentation:** 

> ## ***TERMS***
>> ### OPCODES are basically inbuilt functions in ***EXA***

>>> ### REGISTER are basically variables e.g *x, box* e.tc

>>> ### VALUE are base 10 number

Here a list of them and what they do:

- **load**: load a value or a register into a newly definied register

> **Usage**: `load <value / register> <register>`

- **copy**: copy a value from a register and paste into another already defined register

> **Usage**: `copy <register> <register>`

- **print**: print a string to the screen or print a value from a register_src 
             *if you try `print 10`, it wont print 10 but rather the register with the index 10*

> **Usage**: `print <string / register>`


## ***ARITHMETIC FUNCTIONS***

***Note***: Register must be defined with load before doing arithmetic on them
            *including the register that holds the result*

- **add/sub/muli/div**: add/sub/muli/div two registers together and store the result in another register

> **Usage**: `add / sub / muli / div <register_src1> <register_src2> <register_dest>`
>> **Example**: `add x y x` *x + y = z*

**Note:** The previous architmetic could only work on value in register, these ones works on values in register to values in digits

- **addi/subi/mulii/divi**: add/sub/muli/div a value from a register and a given value and store the result in another register

> **Usage**: `addi / subi / mulii / divi <register_src1> <value> <register_dest>`
>> **Example**: `add x 1 y` * x + 1 = y*

## ***CONDITIONALS***

***Note***: You can mark a **location** in your code by putting ':' after a word e.g `loop:` or `inf:`

- **jump**: jump a marked location in your code when reached
            *goes on forever **ps:** be careful*

> **Usage**: `jump <location>`
>> **Example**: `
                mark:
                jump mark `


