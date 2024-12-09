from ghopper.util.process import Process, CompletedProcess
from ghopper.util.process.error import *
from ghopper.phase_order import PhaseOrder
from ghopper.sequence_importer import SequenceImporter
from ghopper.toolchain.error import *


BENCHMARK_BITCODE_PATH = "/tmp/benchmark.bc"
BENCHMARK_OBJECT_PATH = "/tmp/benchmark.o"
BENCHMARK_BIN_PATH = "/tmp/benchmark"


class Llvm12:
    def __init__(self):
        self.opt_command = ""
        self.llc_command = ""
        self.clang_command = ""
        self.bitcode_path = ""
        self.sequence = ""
        self.process = Process()
        self.sequences_executed = []
        self.sequence_importer = SequenceImporter()

    def optimize(self, bitcode_path, sequence) -> list[PhaseOrder]:
        self.bitcode_path = bitcode_path
        self.sequence = sequence
        self.opt_command = self._get_opt_command()
        self.llc_command = self._get_llc_command()
        self.clang_command = self._get_clang_command()
        self._try_call_commands()
        return self.sequences_executed

    def _try_call_commands(self):
        self._try_run_opt_command()
        self._try_run_llc_command()
        self._try_run_clang_command()

    def _try_run_opt_command(self):
        try:
            completed_process = self.process.run(self.opt_command)
            self.sequences_executed = self._get_sequences_executed(completed_process)
        except CommandNotFoundError as e:
            raise OptNotFoundError(e) from e
        except CommandError as e:
            raise OptError(e) from e

    def _try_run_llc_command(self):
        try:
            self.process.run(self.llc_command)
        except CommandNotFoundError as e:
            raise LlcNotFoundError(e) from e
        except CommandError as e:
            raise LlcError(e) from e

    def _try_run_clang_command(self):
        try:
            self.process.run(self.clang_command)
        except CommandNotFoundError as e:
            raise ClangNotFoundError(e) from e
        except CommandError as e:
            raise ClangError(e) from e

    def _get_sequences_executed(
        self, completed_process: CompletedProcess
    ) -> list[PhaseOrder]:
        assert completed_process
        opt_output = completed_process.stderr
        return self.sequence_importer.from_string(opt_output)

    def _get_opt_command(self):
        assert self.bitcode_path
        assert type(self.sequence) is str, f'Optimization sequence needs to be of type {str}. Received {type(self.sequence)}.'

        return (
            f"opt {self.sequence} --debug-pass=Arguments {self.bitcode_path}"
            f" -o {BENCHMARK_BITCODE_PATH}"
        )

    def _get_llc_command(self):
        return (
            f"llc -filetype=obj {BENCHMARK_BITCODE_PATH}" f" -o {BENCHMARK_OBJECT_PATH}"
        )

    def _get_clang_command(self):
        papi_dir = "/opt/papi/lib"
        return (
            f"clang -lm -L{papi_dir} -lpapi {BENCHMARK_OBJECT_PATH}"
            f" -o {BENCHMARK_BIN_PATH}"
        )
