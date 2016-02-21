import numpy as np

from supplychainpy.demand.abc_xyz import AbcXyz
from supplychainpy.enum_formats import PeriodFormats


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

    def build_window(self, random_normal_demand: list)->dict:
        for sku in self._analysed_orders:
            demand = random_normal_demand[sku.sku_id]

    def closing_stock(self, demand: list) -> list:
      

        return None

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
