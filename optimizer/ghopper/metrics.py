class Metrics:
    def __init__(self):
        self.cpu_cycles = -1
        self.code_size_in_bytes = -1
        self.l1_dcm = None
        self.l1_icm = None
        self.l2_dcm = None
        self.tlb_dm = None
        self.tlb_im = None
        self.hw_int = None
        self.br_msp = None
        self.tot_ins = None
        self.ld_ins = None
        self.sr_ins = None
        self.br_ins = None
        self.l1_dca = None
        self.l2_dca = None

    def __eq__(self, o):
        return (
            self.cpu_cycles == o.cpu_cycles
            and self.code_size_in_bytes == o.code_size_in_bytes
            and self.l1_dcm == o.l1_dcm
            and self.l1_icm == o.l1_icm
            and self.l2_dcm == o.l2_dcm
            and self.tlb_dm == o.tlb_dm
            and self.tlb_im == o.tlb_im
            and self.hw_int == o.hw_int
            and self.br_msp == o.br_msp
            and self.tot_ins == o.tot_ins
            and self.ld_ins == o.ld_ins
            and self.sr_ins == o.sr_ins
            and self.br_ins == o.br_ins
            and self.l1_dca == o.l1_dca
            and self.l2_dca == o.l2_dca
        )

    def __repr__(self):
        return (
            "<Metrics"
            f" cpu_cycles={self.cpu_cycles}"
            f" code_size_in_bytes={self.code_size_in_bytes}"
            f" l1_dcm={self.l1_dcm}"
            f" l1_icm={self.l1_icm}"
            f" l2_dcm={self.l2_dcm}"
            f" tlb_dm={self.tlb_dm}"
            f" tlb_im={self.tlb_im}"
            f" hw_int={self.hw_int}"
            f" br_msp={self.br_msp}"
            f" tot_ins={self.tot_ins}"
            f" ld_ins={self.ld_ins}"
            f" sr_ins={self.sr_ins}"
            f" br_ins={self.br_ins}"
            f" l1_dca={self.l1_dca}"
            f" l2_dca={self.l2_dca}"
            ">"
        )
