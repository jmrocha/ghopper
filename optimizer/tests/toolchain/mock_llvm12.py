from ghopper.toolchain.llvm12 import Llvm12, Llvm12Error
from tests.mock_process import MockProcess


class MockLlvm12(Llvm12):
    def __init__(self):
        self.log = ""
        self._optimize = None
        self.process = MockProcess()
        self._current_value = 0
        self._value = 0
        self._error = None

    def return_optimize(self, value):
        self._optimize = value

    def optimize(self, path: str, sequence: str):
        assert type(sequence) is str
        if self._error and self._current_value == self._value:
            raise self._error
        self._current_value += 1
        return self._optimize

    def raise_error(self, error):
        self._error = error

    def raise_after(self, value):
        self._value = value
