from ghopper.util.process.process import Process
from ghopper.util.process.error import *
from tests.mock_subprocess import *
from unittest import TestCase, skip
import subprocess


class TestProcess(TestCase):
    def setUp(self):
        self.mock_subprocess = MockSubProcess()
        self.process = Process()
        self.process.subprocess = self.mock_subprocess

    def test_run(self):
        completed_process = subprocess.CompletedProcess("", 0)
        completed_process.stdout = "stdout"
        completed_process.stderr = "stderr"
        self.mock_subprocess.return_run(completed_process)
        command = self.process.run("command a b c")
        self.assertEqual(command.stdout, "stdout")
        self.assertEqual(command.stderr, "stderr")
        self.assertEqual(command.exit_code, 0)

    def test_command_not_found(self):
        completed_process = subprocess.CompletedProcess("", 0)
        completed_process.stdout = "stdout"
        completed_process.stderr = "stderr"
        self.mock_subprocess.raise_error(FileNotFoundError)
        with self.assertRaises(CommandNotFoundError):
            self.process.run("bad-command")

    def test_command_error(self):
        error = subprocess.CalledProcessError(-1, "command bad-argument")
        self.mock_subprocess.raise_error(error)
        with self.assertRaises(CommandError):
            self.process.run("command bad-argument")

    def test_subprocess_options(self):
        self.process.run("ls")
        self.assertEqual(self.mock_subprocess.options["capture_output"], True)
        self.assertEqual(self.mock_subprocess.options["check"], True)
        self.assertEqual(self.mock_subprocess.options["text"], True)
        self.assertEqual(self.mock_subprocess.options["encoding"], "utf-8")

    def test_timeout_error(self):
        self.mock_subprocess.raise_error(subprocess.TimeoutExpired("timeout-10s", 10))
        with self.assertRaises(CommandTimeoutError):
            self.process.run("timeout-10s")

    def test_unicode_error(self):
        self.mock_subprocess.raise_error(UnicodeError)
        with self.assertRaises(CommandError):
            self.process.run("unicode")

    def test_define_timeout(self):
        self.process.timeout_in_s = 10
        self.process.run("timeout")
        self.assertEqual(self.mock_subprocess.options["timeout"], 10)

    def test_args(self):
        self.process.run("mycommand a b c")
        self.assertEqual(self.mock_subprocess.command, ["mycommand", "a", "b", "c"])
