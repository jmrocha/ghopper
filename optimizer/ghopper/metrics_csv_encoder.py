class MetricsCSVEncoder:
    def __init__(self):
        self._header = (
                'cpu_cycles,code_size_in_bytes,l1_dcm,l1_icm,l2_dcm,tlb_dm,tlb_im,'
                'hw_int,br_msp,tot_ins,ld_ins,sr_ins,br_ins,l1_dca,l2_dca'
                )

    def encode_header(self):
        return self._header

    def encode_body(self, o):
        metrics = [
                o.cpu_cycles, o.code_size_in_bytes, o.l1_dcm, o.l1_icm, o.l2_dcm,
                o.tlb_dm,o.tlb_im,o.hw_int,o.br_msp,o.tot_ins,o.ld_ins,o.sr_ins,
                o.br_ins,o.l1_dca,o.l2_dca
                ]
        metrics_str_list = [str(metric) for metric in metrics]
        return ",".join(metrics_str_list)
