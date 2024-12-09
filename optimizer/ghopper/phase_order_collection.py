from ghopper.phase_order import PhaseOrder
class PhaseOrderCollection:
    def __init__(self, phase_orders = None):
        self.phase_orders: list[PhaseOrder] = []
        if phase_orders:
            self.phase_orders = phase_orders

    def __iter__(self):
        return iter(self.phase_orders)

    def __getitem__(self, key):
        return self.phase_orders[key]

    def __repr__(self):
        return (
                '<PhaseOrderCollection'
                f' {self.phase_orders}'
                '>')

