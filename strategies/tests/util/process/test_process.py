from unittest import TestCase
from util.process import Process, CommandNotFoundError, CommandInvocationError


class TestProcess(TestCase):
    def setUp(self) -> None:
        self.process = Process()
        self.completed_process = self.process.run("ls -l --color=auto")

    def test_call_external_process(self) -> None:
        self.assertEqual(self.completed_process.exit_code, 0)

    def test_capture_stdout(self) -> None:
        self.assertNotEqual(self.completed_process.stdout, b"")

    def test_capture_stderr(self) -> None:
        self.assertNotEqual(self.completed_process.stderr, b"")

    def test_invalid_invocation(self) -> None:
        with self.assertRaisesRegex(
            CommandInvocationError,
            "ls: invalid-file: No such file or directory\n"
            "Command executed: ls invalid-file",
        ):
            self.process.run("ls invalid-file")

    def test_invalid_command(self) -> None:
        with self.assertRaises(CommandNotFoundError):
            self.process.run("invalid-command")

    def test_decode_utf8_error(self) -> None:
        with self.assertRaises(CommandInvocationError):
            self.process.run("cat tests/resources/example.bc")
