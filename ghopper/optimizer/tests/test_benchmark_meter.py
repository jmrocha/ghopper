from ghopper.benchmark.meter import BenchmarkMeter
from ghopper.util.process import CompletedProcess
from ghopper.util.process.error import CommandTimeoutError
from ghopper.benchmark.meter.error import MeterTimeoutError
from tests.mock_process import MockProcess
from tests.mock_path import MockPath
from unittest import TestCase, skip


class TestBenchmarkMeter(TestCase):
    def setUp(self):
        self.mock_path = MockPath()
        self.mock_process = MockProcess()
        completed_process = CompletedProcess()
        completed_process.stdout = "0 1 2 3 4 5 6 7 8 9 10 11 12 13"
        self.mock_process.return_run(completed_process)
        self.meter = BenchmarkMeter()
        self.meter.process = self.mock_process
        self.meter.path = self.mock_path

    def test_measure(self):
        metrics = self.meter.measure("/tmp/benchmark")
        self.assertEqual(metrics.l1_dcm, 0)
        self.assertEqual(metrics.l1_icm, 1)
        self.assertEqual(metrics.l2_dcm, 2)
        self.assertEqual(metrics.tlb_dm, 3)
        self.assertEqual(metrics.tlb_im, 4)
        self.assertEqual(metrics.hw_int, 5)
        self.assertEqual(metrics.br_msp, 6)
        self.assertEqual(metrics.tot_ins, 7)
        self.assertEqual(metrics.ld_ins, 8)
        self.assertEqual(metrics.sr_ins, 9)
        self.assertEqual(metrics.br_ins, 10)
        self.assertEqual(metrics.cpu_cycles, 11)
        self.assertEqual(metrics.l1_dca, 12)
        self.assertEqual(metrics.l2_dca, 13)

    def test_code_size(self):
        self.mock_path.return_size_in_bytes(10)
        metrics = self.meter.measure("/tmp/benchmark")
        self.assertEqual(metrics.code_size_in_bytes, 10)

    def test_only_cpu_cycles(self):
        completed_process = CompletedProcess()
        completed_process.stdout = "10"
        self.mock_process.return_run(completed_process)
        metrics = self.meter.measure("/tmp/benchmark")
        self.assertEqual(metrics.cpu_cycles, 10)

    def test_timeout_error(self):
        self.mock_process.raise_error(CommandTimeoutError)
        with self.assertRaises(MeterTimeoutError):
            self.meter.measure("./benchmark")

    def test_timeout(self):
        self.meter.timeout_in_s = 2
        self.assertEqual(self.mock_process.get_timeout_in_s(), 2)
