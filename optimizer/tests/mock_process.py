from ghopper.util.process import Process, CompletedProcess
from ghopper.util.process.error import *


class MockProcess(Process):
    def __init__(self):
        super().__init__()
        self.log = ""
        self._run = CompletedProcess()
        self._error = None
        self._value = 0
        self._current_value = 0

    def run(self, command: str):
        self.log += f"{command.split()[0]} "
        if self._error and self._value == self._current_value:
            raise self._error
        self._current_value += 1
        return self._run

    def return_run(self, value: CompletedProcess):
        self._run = value

    def raise_after(self, value):
        self._value = value

    def raise_error(self, error):
        self._error = error
