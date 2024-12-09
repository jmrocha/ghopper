from .completed_process import CompletedProcess
from .error import *
import subprocess


class Process:
    def __init__(self):
        self.command = []
        self.subprocess = subprocess
        self._timeout_in_s = 300  # 5 minutes
        self._subprocess_options = {
            "capture_output": True,
            "check": True,
            "text": True,
            "encoding": "utf-8",
        }

    def _settimeout(self, value_in_s):
        self._timeout_in_s = value_in_s
        self._subprocess_options["timeout"] = value_in_s

    def _gettimeout(self):
        return self._timeout_in_s

    def set_timeout_in_s(self, value):
        self._timeout_in_s = value_in_s
        self._subprocess_options["timeout"] = value_in_s

    def get_timeout_in_s(self):
        return self._timeout_in_s

    timeout_in_s = property(fset=_settimeout, fget=_gettimeout)

    def run(self, command: str) -> CompletedProcess:
        try:
            return self._run_command(command)
        except FileNotFoundError as e:
            raise CommandNotFoundError(e) from e
        except subprocess.TimeoutExpired as e:
            raise CommandTimeoutError(e) from e
        except subprocess.CalledProcessError as e:
            message = ' '.join(e.cmd)
            message += f'\n{e.stderr}'
            raise CommandError(message) from e
        except Exception as e:
            raise CommandError(e) from e

    def _run_command(self, command):
        self.command = command.split()
        res = self.subprocess.run(self.command, **self._subprocess_options)
        return self._get_completed_process(res)

    def _get_completed_process(
        self, x: subprocess.CompletedProcess
    ) -> CompletedProcess:
        completed_process = CompletedProcess()
        completed_process.stdout = x.stdout
        completed_process.stderr = x.stderr
        completed_process.exit_code = x.returncode
        return completed_process
