import sys
import os
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from compiler import Compiler


class TestCompilerPreprocess:
    def setup_method(self):
        self.compiler = Compiler()

    def test_preprocess_removes_comments(self):
        self.compiler.source = self._create_temp_file("print x << comment")
        lines = self.compiler.preprocess()
        assert lines == ["print x"]

    def test_preprocess_removes_standalone_comments(self):
        self.compiler.source = self._create_temp_file("<< comment only")
        lines = self.compiler.preprocess()
        assert lines == []

    def test_preprocess_strips_whitespace(self):
        self.compiler.source = self._create_temp_file("  print x  ")
        lines = self.compiler.preprocess()
        assert lines == ["print x"]

    def test_preprocess_extracts_labels(self):
        self.compiler.source = self._create_temp_file("loop:\nprint x")
        lines = self.compiler.preprocess()
        assert "loop" in self.compiler.LABELS
        assert self.compiler.LABELS["loop"] == 0
        assert lines == ["print x"]

    def test_preprocess_labels_not_counted_as_instructions(self):
        self.compiler.source = self._create_temp_file("loop:\nstart:\nprint x")
        lines = self.compiler.preprocess()
        assert self.compiler.LABELS["loop"] == 0
        assert self.compiler.LABELS["start"] == 0
        assert len(lines) == 1

    def _create_temp_file(self, content):
        fd, path = tempfile.mkstemp(suffix=".ac")
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path


class TestCompilerParse:
    def setup_method(self):
        self.compiler = Compiler()

    def test_parse_load_instruction(self):
        self.compiler.source = self._create_temp_file("load x 42")
        self.compiler.preprocess()
        self.compiler.parse(self.compiler.preprocess())

        assert len(self.compiler.bytecode) == 1
        assert self.compiler.bytecode[0] == [1, 0, 42]

    def test_parse_print_string(self):
        self.compiler.source = self._create_temp_file('print "hello"')
        self.compiler.preprocess()
        self.compiler.parse(self.compiler.preprocess())

        assert len(self.compiler.bytecode) == 1
        assert self.compiler.bytecode[0] == [10, "hello"]

    def test_parse_register_allocation(self):
        self.compiler.source = self._create_temp_file("load x 10\nload y 20")
        self.compiler.preprocess()
        self.compiler.parse(self.compiler.preprocess())

        assert self.compiler.REG["x"] == 0
        assert self.compiler.REG["y"] == 1

    def test_parse_add_instruction(self):
        self.compiler.source = self._create_temp_file("load x 10\nload y 20\nadd x y z")
        self.compiler.preprocess()
        self.compiler.parse(self.compiler.preprocess())

        assert len(self.compiler.bytecode) == 3
        assert self.compiler.bytecode[2] == [2, 0, 1, 2]

    def test_parse_addi_instruction(self):
        self.compiler.source = self._create_temp_file("load x 10\naddi x 5 z")
        self.compiler.preprocess()
        self.compiler.parse(self.compiler.preprocess())

        assert len(self.compiler.bytecode) == 2
        assert self.compiler.bytecode[1] == [6, 0, 5, 1]

    def test_parse_jump_label_resolution(self):
        self.compiler.source = self._create_temp_file("loop:\njump loop")
        lines = self.compiler.preprocess()
        self.compiler.parse(lines)

        assert len(self.compiler.bytecode) == 1
        assert self.compiler.bytecode[0] == [404, 0]

    def test_parse_jumpz_instruction(self):
        self.compiler.source = self._create_temp_file("end:\nload x 0\njumpz end x 0")
        lines = self.compiler.preprocess()
        self.compiler.parse(lines)

        assert len(self.compiler.bytecode) == 2
        assert self.compiler.bytecode[1] == [406, 0, 0, 0]

    def _create_temp_file(self, content):
        fd, path = tempfile.mkstemp(suffix=".ac")
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path


class TestCompilerArgumentValidation:
    def setup_method(self):
        self.compiler = Compiler()

    def test_invalid_instruction_raises_error(self, capsys):
        self.compiler.source = self._create_temp_file("invalid_op x")
        self.compiler.preprocess()
        with pytest.raises(SystemExit):
            self.compiler.parse(self.compiler.preprocess())

    def test_wrong_argument_count_raises_error(self, capsys):
        self.compiler.source = self._create_temp_file("load x")
        self.compiler.preprocess()
        with pytest.raises(SystemExit):
            self.compiler.parse(self.compiler.preprocess())

    def _create_temp_file(self, content):
        fd, path = tempfile.mkstemp(suffix=".ac")
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path
