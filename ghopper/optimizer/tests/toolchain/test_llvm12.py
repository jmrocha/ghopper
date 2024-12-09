from ghopper.phase_order import PhaseOrder
from ghopper.toolchain.llvm12 import *
from ghopper.toolchain.error import *
from ghopper.util.process import CompletedProcess
from ghopper.util.process.error import CommandNotFoundError
from tests.mock_process import *
from unittest import TestCase, skip


class TestLlvm12(TestCase):
    def setUp(self):
        self.toolchain = Llvm12()
        self.mock_process = MockProcess()
        self.toolchain.process = self.mock_process
        completed_process = CompletedProcess()
        completed_process.stderr = (
            "Pass Arguments: -c -b -a\n" "Pass Arguments: -b -a -c"
        )

        self.mock_process.return_run(completed_process)

    def test_opt(self):
        self.toolchain.optimize("./gemm.bc", "-a -b -c")
        self.assertEqual(
            self.toolchain.opt_command,
            "opt -a -b -c --debug-pass=Arguments" " ./gemm.bc -o /tmp/benchmark.bc",
        )

    def test_llc(self):
        self.toolchain.optimize("./gemm.bc", "-a -b -c")
        self.assertEqual(
            self.toolchain.llc_command,
            "llc -filetype=obj /tmp/benchmark.bc -o /tmp/benchmark.o",
        )

    def test_clang(self):
        self.toolchain.optimize("./gemm.bc", "-a -b -c")
        self.assertEqual(
            self.toolchain.clang_command,
            "clang -lm -L/opt/papi/lib -lpapi" " /tmp/benchmark.o -o /tmp/benchmark",
        )

    def test_llvm_commands_order(self):
        self.toolchain.optimize("./gemm.bc", "-a -b -c")
        self.assertEqual(self.mock_process.log, "opt llc clang ")

    def test_parse_opt_output(self):
        completed_process = CompletedProcess()
        completed_process.stderr = (
            "Pass Arguments: -c -b -a\n" "Pass Arguments: -b -a -c"
        )
        self.mock_process.return_run(completed_process)
        sequences_executed = self.toolchain.optimize("./gemm.bc", "-a -b -c")
        self.assertEqual(
            sequences_executed, [PhaseOrder("-c -b -a"), PhaseOrder("-b -a -c")]
        )

    def test_opt_error(self):
        self.mock_process.raise_error(CommandError)
        with self.assertRaises(OptError):
            self.toolchain.optimize("./gemm.bc", "-a -b -c")

    def test_llc_error(self):
        self.mock_process.raise_error(CommandError)
        self.mock_process.raise_after(1)
        with self.assertRaises(LlcError):
            self.toolchain.optimize("./gemm.bc", "-a -b -c")

    def test_opt_not_found(self):
        self.mock_process.raise_error(CommandNotFoundError)
        with self.assertRaises(OptNotFoundError):
            self.toolchain.optimize("./gemm.bc", "-a")

    def test_llc_not_found(self):
        self.mock_process.raise_error(CommandNotFoundError)
        self.mock_process.raise_after(1)
        with self.assertRaises(LlcNotFoundError):
            self.toolchain.optimize("./gemm.bc", "-a")

    def test_clang_not_found(self):
        self.mock_process.raise_error(CommandNotFoundError)
        self.mock_process.raise_after(2)
        with self.assertRaises(ClangNotFoundError):
            self.toolchain.optimize("./gemm.bc", "-a")

    def test_bitcode_without_main(self):
        self.mock_process.raise_error(CommandError)
        self.mock_process.raise_after(2)
        with self.assertRaises(ClangError):
            self.toolchain.optimize("./gemm.bc", "-a -b -c")
