import subprocess
from subprocess import CalledProcessError
from .command_not_found_error import CommandNotFoundError
from .command_invocation_error import CommandInvocationError
from .completed_process import CompletedProcess


class Process:
    def run(self, command: str) -> CompletedProcess:
        self._command = command
        return self._run()

    def _run(self) -> CompletedProcess:
        try:
            return self._try_run()
        except FileNotFoundError as e:
            self._handle_command_not_found(e)
        except CalledProcessError as e:
            self._handle_called_process_error(e)
        except UnicodeDecodeError as e:
            self._handle_unicode_decode_error(e)

    def _try_run(self) -> CompletedProcess:
        completed_process = self.run_process()
        result = CompletedProcess()
        result.exit_code = completed_process.returncode
        result.stdout = completed_process.stdout
        result.stderr = completed_process.stderr
        return result

    def run_process(self) -> subprocess.CompletedProcess:
        return subprocess.run(self.command(), **self._options)

    def command(self):
        command_array = self._command.split(" ")
        return [argument for argument in command_array if argument != ""]

    def _handle_command_not_found(self, e: FileNotFoundError) -> None:
        raise CommandNotFoundError(e)

    def _handle_called_process_error(self, e: CalledProcessError) -> None:
        stderr = "".join(e.stderr.splitlines())
        error = f"{stderr}\nCommand executed: {self._command}"
        raise CommandInvocationError(error)

    def _handle_unicode_decode_error(self, e: UnicodeDecodeError) -> None:
        error = f"Couldn't decode the process output using utf-8.\nCommand executed: {self._command}"
        raise CommandInvocationError(error)

    def __init__(self) -> None:
        self._command: str = ""
        self._options: dict[str, Any] = {
            # capture output from stdout and stderr
            "capture_output": True,
            # raise error if the process exits with a non-zero code
            "check": True,
            # decode stdout and stderr
            "text": True,
            "encoding": "utf-8",
        }
