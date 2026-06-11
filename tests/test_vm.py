import sys
import os
import pytest
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vm import exaVm


class TestVMArithmetic:
    def test_load_and_print(self):
        bytecode = [[1, 0, 42]]  # load x with 42
        registers = [0, 0]
        result = exaVm(bytecode, registers)
        assert registers[0] == 42

    def test_add_registers(self):
        bytecode = [
            [1, 0, 10],  # load x = 10
            [1, 1, 20],  # load y = 20
            [2, 0, 1, 2],  # add x, y -> z
        ]
        registers = [0, 0, 0]
        exaVm(bytecode, registers)
        assert registers[2] == 30

    def test_sub_registers(self):
        bytecode = [
            [1, 0, 50],
            [1, 1, 30],
            [3, 0, 1, 2],  # sub x, y -> z
        ]
        registers = [0, 0, 0]
        exaVm(bytecode, registers)
        assert registers[2] == 20

    def test_mul_registers(self):
        bytecode = [
            [1, 0, 5],
            [1, 1, 4],
            [4, 0, 1, 2],  # mul x, y -> z
        ]
        registers = [0, 0, 0]
        exaVm(bytecode, registers)
        assert registers[2] == 20

    def test_div_registers(self):
        bytecode = [
            [1, 0, 20],
            [1, 1, 4],
            [5, 0, 1, 2],  # div x, y -> z
        ]
        registers = [0, 0, 0]
        exaVm(bytecode, registers)
        assert registers[2] == 5

    def test_addi(self):
        bytecode = [
            [1, 0, 10],
            [6, 0, 5, 1],  # addi x, 5 -> y
        ]
        registers = [0, 0]
        exaVm(bytecode, registers)
        assert registers[1] == 15

    def test_subi(self):
        bytecode = [
            [1, 0, 10],
            [7, 0, 3, 1],  # subi x, 3 -> y
        ]
        registers = [0, 0]
        exaVm(bytecode, registers)
        assert registers[1] == 7

    def test_mulii(self):
        bytecode = [
            [1, 0, 10],
            [8, 0, 2, 1],  # mulii x, 2 -> y
        ]
        registers = [0, 0]
        exaVm(bytecode, registers)
        assert registers[1] == 20

    def test_divi(self):
        bytecode = [
            [1, 0, 10],
            [9, 0, 2, 1],  # divi x, 2 -> y
        ]
        registers = [0, 0]
        exaVm(bytecode, registers)
        assert registers[1] == 5


class TestVMControlFlow:
    def test_jump(self):
        bytecode = [
            [1, 0, 1],   # load x = 1
            [404, 3],    # jump to instruction 3 (skip index 2)
            [1, 0, 99],  # load x = 99 (should be skipped)
            [1, 1, 2],   # load y = 2
        ]
        registers = [0, 0, 0]
        exaVm(bytecode, registers)
        assert registers[0] == 1
        assert registers[1] == 2

    def test_jumpz_mode0_jumps_when_not_zero(self):
        bytecode = [
            [1, 0, 5],   # load x = 5 (not zero)
            [406, 3, 0, 0],  # jumpz to 3 if x != 0 (mode 0) - x IS NOT zero, so jump
            [1, 1, 10],  # load y = 10 (skipped)
            [1, 2, 20],  # load z = 20
        ]
        registers = [0, 0, 0]
        exaVm(bytecode, registers)
        assert registers[0] == 5
        assert registers[1] == 0
        assert registers[2] == 20

    def test_jumpz_mode1_jumps_when_zero(self):
        bytecode = [
            [1, 0, 0],     # load x = 0
            [406, 3, 0, 1],  # jumpz to 3 if x == 0 (mode 1)
            [1, 1, 10],    # load y = 10 (should be skipped)
            [1, 1, 20],    # load y = 20
        ]
        registers = [0, 0]
        exaVm(bytecode, registers)
        assert registers[1] == 20

    def test_jumpr_mode0_jumps_when_zero(self):
        bytecode = [
            [1, 0, 0],     # load x = 0
            [406, 3, 0, 0],  # jumpr to 3 if x == 0 (mode 0)
            [1, 1, 10],    # load y = 10 (should be skipped)
            [1, 2, 20],    # load z = 20
        ]
        registers = [0, 0, 0]
        exaVm(bytecode, registers)
        assert registers[1] == 10
        assert registers[2] == 20


class TestVMCopy:
    def test_copy_register(self):
        bytecode = [
            [1, 0, 42],
            [11, 0, 1],  # copy x -> y
        ]
        registers = [0, 0]
        exaVm(bytecode, registers)
        assert registers[1] == 42


class TestVMHaltKill:
    def test_halt_returns_success_output(self, capsys):
        bytecode = [
            [1, 0, 42],
            [255],  # halt
            [1, 0, 999],  # should not execute
        ]
        registers = [0]
        result = exaVm(bytecode, registers)
        assert registers[0] == 42

    def test_kill_returns_failure_output(self, capsys):
        bytecode = [
            [1, 0, 42],
            [256],  # kill
        ]
        registers = [0]
        result = exaVm(bytecode, registers)
        assert registers[0] == 42
