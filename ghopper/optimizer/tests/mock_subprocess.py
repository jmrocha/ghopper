import subprocess


class MockSubProcess:
    def __init__(self):
        self._error = None
        self._run = subprocess.CompletedProcess("", 0)
        self.options = {}
        self.command = []

    def run(self, command, **kwargs):
        self.command = command
        self.options = dict(kwargs)
        if self._error:
            raise self._error
        return self._run

    def raise_error(self, error):
        self._error = error

    def return_run(self, value):
        self._run = value
