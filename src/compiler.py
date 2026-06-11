# pyright: reportMissingImports=false
import sys

from settings import OPCODES, color, ARG
from utils import error, genBytecode


class Compiler:
    def __init__(self):
        self.REG = {}
        self.register_count = 0
        self.LABELS = {}
        self.instruction_index = 0
        self.bytecode = []
        self.source = ""

    def preprocess(self) -> list:
        lines = []

        with open(self.source, "r") as f:
            for raw_line in f:
                if "<<" in raw_line:
                    raw_line = raw_line.split("<<")[0]

                line = raw_line.strip()
                if not line:
                    continue

                # Label (do NOT count as instruction)
                if line.endswith(":"):
                    label_name = line[:-1].lower()
                    self.LABELS[label_name] = self.instruction_index
                    continue

                # Real instruction
                lines.append(line)
                self.instruction_index += 1
        return lines

    # source = validate_file()
    # lines = preprocess(source)

    def process_args(self, parts, instruction, instruction_bytes):

        instruction_bytes.append(OPCODES[instruction])

        # Handle jump instructions specially
        if instruction == "jump":
            # First arg is always a label (may be forward reference)
            arg = parts[1].lower()
            instruction_bytes.append(self.LABELS.get(arg, arg))
            return instruction_bytes

        if instruction == "jumpz":
            # Format: jumpz <label> <register> <mode>
            label_arg = parts[1].lower()
            instruction_bytes.append(self.LABELS.get(label_arg, label_arg))
            # Register arg
            reg_arg = parts[2].lower()
            if reg_arg not in self.REG:
                self.REG[reg_arg] = self.register_count
                self.register_count += 1
            instruction_bytes.append(self.REG[reg_arg])
            # Mode arg (number)
            instruction_bytes.append(int(parts[3]))
            return instruction_bytes

        # Add any args before the string
        for i in range(1, len(parts)):
            arg = parts[i].lower()

            # Is it a label reference?
            if arg in self.LABELS:
                instruction_bytes.append(self.LABELS[arg])

            # Is it a register?
            elif arg.isalpha():
                if arg not in self.REG:
                    self.REG[arg] = self.register_count
                    self.register_count += 1
                instruction_bytes.append(self.REG[arg])
            else:
                instruction_bytes.append(int(arg))
        return instruction_bytes

    def parse(self, lines):
        for line in lines:
            instruction_bytes = []

            if '"' in line:
                # split the string
                quote = line.split('"')
                before_quote = quote[0].strip()
                string_content = quote[1]
                parts = before_quote.split()

            else:
                # Normal instruction (no string)
                parts = line.split()
                instruction = parts[0].lower()
                args = parts[1:]
                string_content = None
                expected = ARG.get(instruction, None)
                if expected is not None and len(args) != expected:
                    print(
                        f"{color['r']}Error: '{instruction}' expects {expected} arguments, got {len(args)}{color['reset']}"
                    )
                    sys.exit(1)

            instruction = parts[0].lower()

            if instruction not in OPCODES:
                error("unknown instruction", self.instruction_index)
                sys.exit(1)

            instruction_bytes = self.process_args(parts, instruction, instruction_bytes)

            if string_content is not None:
                instruction_bytes.append(string_content)

            self.bytecode.append(instruction_bytes)

    def resolve_labels(self):
        for instruction in self.bytecode:
            opcode = instruction[0]
            if opcode == 404:  # jump
                target = instruction[1]
                if isinstance(target, str):
                    instruction[1] = self.LABELS.get(target, target)
            elif opcode == 406:  # jumpz
                target = instruction[1]
                if isinstance(target, str):
                    instruction[1] = self.LABELS.get(target, target)

    def compile(self, source: str, debug: bool = False) -> list:
        self.source = source
        self.debug = debug
        lines = self.preprocess()
        self.parse(lines)
        self.resolve_labels()
        if self.debug:
            genBytecode(source, self.bytecode)
        return self.bytecode
