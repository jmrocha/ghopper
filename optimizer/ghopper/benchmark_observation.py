from ghopper.metrics import Metrics
from ghopper.phase_order import PhaseOrder
from ghopper.phase_order_collection import PhaseOrderCollection


class BenchmarkObservation:
    def __init__(self):
        self.benchmark_name = ""
        self.phase_order_requested = PhaseOrder()
        self.phase_orders_executed = PhaseOrderCollection()
        self.metrics = Metrics()
        self.has_error = False
        self.error = ''

    def __repr__(self):
        return (
            "<BenchmarkObservation"
            f' {self.benchmark_name=}'
            f"  {self.metrics=}"
            f"  {self.phase_order_requested=}"
            f"  {self.phase_orders_executed=}"
            f' {self.has_error=}'
            f' {self.error=}'
            ">"
        )
