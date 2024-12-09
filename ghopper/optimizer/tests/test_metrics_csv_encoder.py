from ghopper.metrics_csv_encoder import MetricsCSVEncoder
from ghopper.metrics import Metrics
from unittest import TestCase


class TestMetricsCSVEncoder(TestCase):
    def test_encode_header(self):
        encoder = MetricsCSVEncoder()
        self.assertEqual(encoder.encode_header(),
                "cpu_cycles,code_size_in_bytes"
                ',l1_dcm,l1_icm,l2_dcm,tlb_dm,tlb_im,hw_int,br_msp,tot_ins,ld_ins'
                ',sr_ins,br_ins,l1_dca,l2_dca'
                )

    def test_encode_body(self):
        encoder = MetricsCSVEncoder()
        metrics = Metrics()
        metrics.cpu_cycles = 0
        metrics.code_size_in_bytes = 1 
        metrics.l1_dcm = 2
        metrics.l1_icm = 3
        metrics.l2_dcm = 4
        metrics.tlb_dm = 5
        metrics.tlb_im = 6
        metrics.hw_int = 7
        metrics.br_msp = 8
        metrics.tot_ins =9 
        metrics.ld_ins = 10
        metrics.sr_ins = 11
        metrics.br_ins = 12
        metrics.l1_dca = 13
        metrics.l2_dca = 14
        encoded = encoder.encode_body(metrics)
        self.assertEqual(encoded, ','.join([str(x) for x in range(15)]))
