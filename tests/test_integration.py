import sys
import os
import tempfile
import pytest
from io import StringIO

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from compiler import Compiler
from vm import exaVm


def create_temp_ac_file(content):
    fd, path = tempfile.mkstemp(suffix=".ac")
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return path


def compile_source(source):
    compiler = Compiler()
    compiler.source = source
    lines = compiler.preprocess()
    compiler.parse(lines)
    registers = [0] * compiler.register_count
    return compiler.bytecode, registers


def test_hello_world():
    source = create_temp_ac_file('print "hello world"')
    bytecode, registers = compile_source(source)
    result = exaVm(bytecode, registers)
    assert "hello world" in result


def test_simple_arithmetic():
    source = create_temp_ac_file("""
load x 10
load y 5
add x y z
print z
halt
""")
    bytecode, registers = compile_source(source)
    result = exaVm(bytecode, registers)
    assert "15" in result


def test_string_loading():
    source = create_temp_ac_file('sload name "Alice"\nprint name\nhalt')
    bytecode, registers = compile_source(source)
    result = exaVm(bytecode, registers)
    assert "Alice" in result


def test_concat_strings():
    source = create_temp_ac_file("""
sload first "Hello"
sload second "World"
sload result "placeholder"
concat first second result
print result
halt
""")
    bytecode, registers = compile_source(source)
    result = exaVm(bytecode, registers)
    assert "HelloWorld" in result


def test_simple_loop():
    source = create_temp_ac_file("""
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
""")
    bytecode, registers = compile_source(source)
    result = exaVm(bytecode, registers)
    assert "3" in result
    assert "done" in result


def test_copy_instruction():
    source = create_temp_ac_file("""
load x 42
copy x y
print y
halt
""")
    bytecode, registers = compile_source(source)
    result = exaVm(bytecode, registers)
    assert "42" in result


def test_all_arithmetic_ops():
    source = create_temp_ac_file("""
load a 10
load b 3
load c 0
load d 0
load e 0
load f 0
add a b c
sub a b d
muli a b e
div a b f
print c
print d
print e
print f
halt
""")
    bytecode, registers = compile_source(source)
    result = exaVm(bytecode, registers)
    assert "13" in result  # 10 + 3
    assert "7" in result   # 10 - 3
    assert "30" in result  # 10 * 3
    assert "3" in result   # 10 / 3 (floor)


def test_immediate_arithmetic():
    source = create_temp_ac_file("""
load x 5
load a 0
load b 0
load c 0
load d 0
addi x 10 a
subi x 2 b
mulii x 3 c
divi x 2 d
print a
print b
print c
print d
halt
""")
    bytecode, registers = compile_source(source)
    result = exaVm(bytecode, registers)
    assert "15" in result  # 5 + 10
    assert "3" in result  # 5 - 2
    assert "15" in result  # 5 * 3
    assert "2" in result   # 5 / 2 (floor)
