from ghopper.util.path import Path
from ghopper.util.process import Process
from ghopper.metrics import Metrics
from ghopper.util.process.error import CommandTimeoutError, CommandNotFoundError
from ghopper.benchmark.meter.error import *


class BenchmarkMeter:
    def __init__(self):
        self.process = Process()
        self.path = Path()
        self._timeout_in_s = 300

    def _settimeout(self, value):
        self._timeout_in_s = value
        self.process.timeout_in_s = value

    def get_timeout_in_s(self):
        return self._timeout_in_s

    timeout_in_s = property(fset=_settimeout)

    def measure(self, executable_path: str) -> Metrics:
        executable_output = self._run_executable(executable_path)
        metrics = self._get_metrics_from_output(executable_output)
        metrics.code_size_in_bytes = self.path.size_in_bytes(executable_path)
        return metrics

    def _run_executable(self, path: str) -> str:
        try:
            return self.process.run(path).stdout
        except CommandTimeoutError as e:
            raise MeterTimeoutError(e) from e
        except CommandNotFoundError as e:
            raise MeterError(e) from e

    def _get_metrics_from_output(self, output: str) -> Metrics:
        metrics_list = self._get_metrics_list_from_output(output)
        metrics = Metrics()
        if len(metrics_list) > 1:
            metrics.l1_dcm = metrics_list[0]
            metrics.l1_icm = metrics_list[1]
            metrics.l2_dcm = metrics_list[2]
            metrics.tlb_dm = metrics_list[3]
            metrics.tlb_im = metrics_list[4]
            metrics.hw_int = metrics_list[5]
            metrics.br_msp = metrics_list[6]
            metrics.tot_ins = metrics_list[7]
            metrics.ld_ins = metrics_list[8]
            metrics.sr_ins = metrics_list[9]
            metrics.br_ins = metrics_list[10]
            metrics.cpu_cycles = metrics_list[11]
            metrics.l1_dca = metrics_list[12]
            metrics.l2_dca = metrics_list[13]
        else:
            metrics.cpu_cycles = metrics_list[0]
        return metrics

    def _get_metrics_list_from_output(self, output: str):
        return [int(x) for x in output.split()]
