import numpy as np

from supplychainpy.demand.abc_xyz import AbcXyz
from supplychainpy.enum_formats import PeriodFormats
from supplychainpy.simulations import simulation_window


# assumptions: opening stock in first period is average stock adjusted to period used in monte carlo if different from
# orders analysis. There are no deliveries in the first period (maybe add sitch so there always is a delivery in first
# period based on inventory rules.

class SetupMonteCarlo:
    _conversion = 1
    _window = {}

    def __init__(self, analysed_orders: AbcXyz, period: str = PeriodFormats.months.name):
        self._analysed_orders = analysed_orders

    # pass the period and length of period. The period has to be set in the orders data so the
    # conversion can be made if necessary. run

    def generate_normal_random_distribution(self, period_length: int) -> list:
        orders_normal_distribution = {}
        random_orders_generator = []
        final_random_orders_generator = []
        for sku in self._analysed_orders:
            for i in range(0, period_length):
                nrd_orders = np.random.normal(loc=sku.average_orders,
                                              scale=sku.standard_deviation,
                                              size=sku.order_count)

                random_orders_generator.append([abs(nrd_orders)])
            orders_normal_distribution[sku.sku_id] = random_orders_generator
            random_orders_generator = []
        final_random_orders_generator.append(orders_normal_distribution)
        return final_random_orders_generator

    def build_window(self, random_normal_demand: list, period_length: int = 0) -> dict:
        closing_stock = lambda opening_stock, orders, deliveries: (opening_stock - orders) + deliveries
        backlog = lambda cls_stock: abs(cls_stock) if cls_stock < 0 else 0

        for sku in self._analysed_orders:
            for i in range(0, period_length):
                sim_window = simulation_window.MonteCarloWindow
                sim_window.closing_stock = closing_stock(sim_window.opening_stock, random_normal_demand[sku.sku_id][0],
                                                         sim_window.purchase_order_receipt_qty)
                sim_window.backlog = backlog(sim_window.closing_stock)


    def _normal_random_distribution_cuda(self, num_runs: int) -> dict:
        pass

    def _covert_period(self, period) -> bool:
        pass

    def _opening_stock(self):
        pass

    def _delivery(self):
        pass

    def _backlog(self):
        pass

    def _holding_cost(self):
        pass

    def _shortage_cost(self):
        pass

    def _po_placement(self):
        pass

    def _po_receipt(self):
        pass
