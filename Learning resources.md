# Learning Path: Build Your Own Computer

## Goal
Design EXA into hardware. Create a CPU that runs EXA bytecode natively.

---

## Phase 1: Fundamentals (Weeks 1-4)

### Digital Logic
- **NandGame** (nandgame.com) - Build a computer from NAND gates in your browser. Free.
- **LinkedIn Learning / YouTube** - Search "digital logic basics"
- Learn: gates (AND, OR, NOT, XOR), truth tables, boolean algebra

### Computer Architecture Basics
- **Nand to Tetris Part 1** (coursera.org) - Free to audit
  - Build a CPU from scratch using HDL
  - 6-week course, 5-8 hours/week
  - By end: you have a working 16-bit computer
- **nand2tetris.org** - Book + site, free resources

---

## Phase 2: CPU Design (Weeks 5-10)

### HDL (Hardware Description Language)
- **Logisim Evolution** (logisim.org) - Free, visual circuit simulator
  - Design your CPU schematic visually
  - No programming required
- **Verilog/VHDL** (optional, for real FPGAs)
  - **HDLBits** (hdlbits.01xz.net) - Free Verilog exercises
  - **NandLand** (nandland.com) - Intro to FPGAs and Verilog

### Architecture Concepts
- **Coursera: Computer Architecture** - Princeton (free to audit)
- **YouTube: Building a Simple CPU** - Multiple channels cover this
- Learn: instruction cycle, fetch/decode/execute, registers, memory bus

### Define Your ISA
- Document EXA bytecode as binary encoding
- Example:
  - `load reg value` → `0001 [reg] [value as 32-bit int]`
  - `add a b c` → `0010 [a] [b] [c]`
- Keep it simple. 16-bit or 32-bit instruction width.

---

## Phase 3: Implementation (Weeks 11-20)

### FPGA Development (~$20-50)
- **Lattice iCE40** boards - cheapest, open source toolchain
  - IceStorm / NextPNR - free open source tools
- **Quartus** (Intel) - Free version for Cyclone chips
- **Vivado** (Xilinx) - Free version for Artix-7

### Options by Budget
| Budget | Option |
|--------|--------|
| $0 | Simulation only (Logisim, Verilator) |
| $15-20 | Lattice iCE40 FPGA board |
| $30-50 | MAX10 or Artix-7 board |
| $100+ | Full PCB fabrication |

### Build Pipeline
1. Design in Logisim → test in simulation
2. Write Verilog/VHDL
3. Synthesize for FPGA
4. Flash to board
5. Debug with LEDs/7-segments

---

## Phase 4: Integration (Weeks 21+)

### From VM to Hardware
- Write EXA compiler that outputs your binary ISA
- Port EXA VM logic to hardware description
- Test bytecode on real hardware
- Add peripherals: UART (serial), GPIO, maybe VGA

### Peripherals
- **Embedded Systems** course on Coursera
- **SPI/I2C** - Search YouTube, straightforward protocols
- Start with LEDs and switches, upgrade to display

---

## Free Tools Summary

| Tool | Purpose | Cost |
|------|---------|------|
| NandGame | Logic gates intro | Free |
| Nand2Tetris | Full CPU design | Free |
| Logisim | Circuit simulation | Free |
| HDLBits | Verilog practice | Free |
| Wokwi | Arduino/Pico simulator | Free |
| Verilator | HDL simulation | Free |
| IceStorm | FPGA toolchain | Free |
| NextPNR | FPGA place+route | Free |

---

## Recommended Order

1. NandGame (1-2 days)
2. Nand2Tetris Part 1 (6 weeks)
3. Design EXA ISA on paper
4. Logisim CPU design (ongoing)
5. Optional FPGA when ready

---

## Key Communities

- **r/askelectronics** - Questions and help
- **r/FPGA** - Hardware discussion
- **r/osdev** - OS development (your future project)
- **hackaday.com** - Hardware projects
- ** MightyZtin (Discord)** - Embedded/hardware

---

## Realistic Timeline

- 0-2 months: Fundamentals
- 3-4 months: CPU design in simulation
- 5-6 months: First FPGA implementation
- 6+ months: Integration, peripherals, polish

---

## If You Get Stuck

- Break it into smaller pieces
- Search YouTube for specific terms
- Ask on Reddit with a clear question
- Google the error message

---

Start with NandGame tonight. 30 minutes. You'll understand gates by the end.
