import numpy as np

from supplychainpy.demand.abc_xyz import AbcXyz
from supplychainpy.enum_formats import PeriodFormats


class SetupMonteCarlo:
    def __init__(self, analysed_orders: AbcXyz, period: str = PeriodFormats.months.name):
        self._analysed_orders = analysed_orders
        self._normal_random_distribution = self._normal_random_distribution()

    @property
    def normal_random_distribution(self):
        return self._normal_random_distribution

    # pass the period and length of period. The period has to be set in the orders data so the
    # conversion can be made if necessary. run

    def _normal_random_distribution(self) -> dict:
        orders_normal_distribution = {}
        for sku in self._analysed_orders:
            nrd_orders = np.random.normal(loc=sku.average_orders,
                                          scale=sku.standard_deviation,
                                          size=sku.order_count)

            orders_normal_distribution[sku.sku_id] = nrd_orders
        return orders_normal_distribution

    def _normal_random_distribution_cuda(self, num_runs: int) -> dict:
        pass

    def _convert_period(self):
        pass
