from decimal import Decimal
from collections import Iterable
import collections

from supplychainpy.enum_formats import PeriodFormats
order = collections.namedtuple('order', 'sku sku_orders')


def _standard_deviation_orders(orders: dict, average_order: Decimal) -> Decimal:
    deviation = Decimal(0)
    variance = []
    for x in orders.values():
        variance.append(Decimal(x - average_order))
    for j in variance:
        deviation += Decimal(j) ** Decimal(2)
    deviation /= Decimal(len(variance))
    return Decimal(Decimal(deviation) ** Decimal(0.5))


class UncertainDemand:
    """ Models inventory profile calculating economic order quantity, variable cost, reorder quantity and
        ABCXYZ classification
    """
    __z_value = Decimal(0.00)  # default set to 90%
    __lead_time = 0
    __safety_stock = 0
    __demand_variability = Decimal(0)
    __reorder_level = 0
    __unit_cost = Decimal(0.00)
    __reorder_cost = Decimal(00.00)
    __CONST_HOLDING_COST_FACTOR = Decimal(0.25)
    __fixed_reorder_quantity = 0
    __DAYS = Decimal(7)
    __WEEKS = Decimal(4)
    __MONTHS = Decimal(12)
    __QUARTER = Decimal(4)
    __period = 0
    __sku_revenue = Decimal(0)
    __percentage_of_revenue = Decimal(0)
    __cumulative_percentage = Decimal(0)
    __abc_classification = ""
    __xyz_classification = ""
    __economic_order_variable_cost = Decimal(0)
    __economic_order_qty = Decimal(0)

    def __init__(self, orders: dict, sku: str, lead_time: Decimal, unit_cost: Decimal, reorder_cost: Decimal,
                 z_value: Decimal = Decimal(1.28), holding_cost: Decimal = 0.00,
                 period: str = PeriodFormats.months.name):

        self.__orders = orders
        self.__sku_id = sku
        self.__lead_time = Decimal(lead_time)
        self.__unit_cost = Decimal(unit_cost)
        self.__z_value = z_value
        self.__count_orders = len(self.__orders)

        if len(orders) < 2:
            self.__average_order = Decimal(self.average_order_row())
            self.__orders_standard_deviation = self._standard_deviation_orders_row()
        else:
            self.__average_order = Decimal(self.average_order())
            self.__orders_standard_deviation = _standard_deviation_orders(orders=orders,
                                                                          average_order=self.__average_order)
        self.__sku_revenue = self._revenue(orders=orders)
        self.__safety_stock = self._safety_stock()
        self.__demand_variability = self._demand_variability()
        self.__reorder_level = Decimal(self._reorder_level())
        self.__reorder_cost = Decimal(reorder_cost)
        self.__fixed_reorder_quantity = Decimal(self._fixed_order_quantity())
        self.__order = [order(sku, sku_orders) for sku_orders in self.__orders for sku in self.__sku_id]
        self.__period = period


    @property
    def safety_stock(self):
        return self.__safety_stock

    @safety_stock.setter
    def safety_stock(self, safety_stock):
        self.__safety_stock = safety_stock

    @property
    def reorder_level(self):
        return self.__reorder_level

    @reorder_level.setter
    def reorder_level(self, reorder_level):
        self.__reorder_level = reorder_level

    @property
    def unit_cost(self)->Decimal:
        return self.__unit_cost

    @unit_cost.setter
    def unit_cost(self, unit_cost):
        self.__unit_cost = unit_cost

    @property
    def abcxyz_classification(self) -> str:
        """Gets ABCXYZ classification as a concatenated string"""
        return self.__abc_classification + self.__xyz_classification


    @property
    def abc_classification(self) -> str:
        return self.__abc_classification

    @abc_classification.setter
    def abc_classification(self, abc_classifier: str):
        self.__abc_classification = abc_classifier

    @property
    def xyz_classification(self) -> str:
        return self.__xyz_classification

    @xyz_classification.setter
    def xyz_classification(self, xyz_classifier: str):
        self.__xyz_classification = xyz_classifier

    @property
    def percentage_revenue(self) -> Decimal:
        return self.__percentage_of_revenue

    @percentage_revenue.setter
    def percentage_revenue(self, percentage_orders):
        self.__percentage_of_revenue = percentage_orders

    @property
    def cumulative_percentage(self) -> Decimal:
        return self.__cumulative_percentage

    @cumulative_percentage.setter
    def cumulative_percentage(self, percentage_orders):
        self.__cumulative_percentage = percentage_orders

    @property
    def order(self):
        total_order = 0
        orders_list = []
        for items in self.__orders:
            orders_list = self.__orders[items]
        if isinstance(orders_list, Iterable):
            for item in orders_list:
                total_order += Decimal(item)
        else:
            for item in self.__orders:
                total_order += self.__orders[item]
        return total_order

    @property
    def order_count(self):
        return self.__count_orders

    @order.setter
    def order(self, orders):
        self.__orders = orders

    @property
    def sku_id(self):
        return self.__sku_id

    @sku_id.setter
    def sku_id(self, sku):
        self.__sku_id = sku

    @property
    def lead_time(self):
        return self.__lead_time

    @lead_time.setter
    def lead_time(self, lead_time):
        self.__lead_time = lead_time

    @property
    def average_orders(self):
        return self.__average_order

    @property
    def standard_deviation(self):
        return self.__orders_standard_deviation

    @property
    def revenue(self) -> Decimal:
        return self.__sku_revenue

    @property
    def demand_variability(self) -> Decimal:
        return self._demand_variability()

    @demand_variability.setter
    def demand_variability(self, demand_variability: Decimal):
        self.__demand_variability = demand_variability

    @property
    def fixed_order_quantity(self):
        return self.__fixed_reorder_quantity

    @fixed_order_quantity.setter
    def fixed_order_quantity(self, order):
        self.__fixed_reorder_quantity = order

    @property
    def economic_order_qty(self):
        return self.__economic_order_qty

    @economic_order_qty.setter
    def economic_order_qty(self, eoq):
        self.__economic_order_qty = eoq

    @property
    def economic_order_variable_cost(self) -> Decimal:
        return self.__economic_order_variable_cost

    @economic_order_variable_cost.setter
    def economic_order_variable_cost(self, eoq_vc):
        self.__economic_order_variable_cost = eoq_vc

    def average_order(self):
        return float(sum(self.__orders.values()) / self.__count_orders)

    def average_order_row(self) -> Decimal:
        total_orders = 0
        for item in self.__orders:
            orders_list = self.__orders[item]
        for item in orders_list:
            total_orders += Decimal(item)
        return Decimal(total_orders / len(orders_list))

    def _revenue(self, orders: dict) -> Decimal:
        total_order = 0
        for items in orders:
            orders_list = orders[items]
        if isinstance(orders_list, Iterable):
            for item in orders_list:
                total_order += Decimal(item)
        else:
            for item in orders:
                total_order += orders[item]

        return Decimal(total_order * Decimal(self.__unit_cost))

    def _standard_deviation_orders_row(self) -> Decimal:
        deviation = Decimal(0)
        variance = []
        for item in self.__orders:
            orders_list = self.__orders[item]
        for item in orders_list:
            variance.append(Decimal(Decimal(item) - Decimal(self.__average_order)))
        for j in variance:
            deviation += Decimal(j) ** Decimal(2)
        deviation /= Decimal(len(variance))
        return Decimal(Decimal(deviation) ** Decimal(0.5))

    # TODO-feature convert lead-time to correct period (data_set period must match lead_time priod if not conversion)
    def _safety_stock(self) -> Decimal:
        return Decimal(self.__z_value) * Decimal(self.__orders_standard_deviation) * Decimal(
            (self.__lead_time ** Decimal(0.5)))

    def _demand_variability(self) -> Decimal:
        return Decimal(Decimal(self.__orders_standard_deviation) / Decimal(self.__average_order))

    def _reorder_level(self) -> Decimal:
        return (Decimal(self.__lead_time ** Decimal(0.5)) * Decimal(self.__average_order)) + Decimal(
            self.__safety_stock)

    # provide the facility to output order quantity as a range if the reorder cost is an estimation
    # one version when holding cost has not been specified and one when it has been
    def _fixed_order_quantity(self) -> Decimal:
        return (2 * Decimal(self.__reorder_cost) * (
            Decimal(self.__average_order) / (
                Decimal(self.__unit_cost) * Decimal(self.__CONST_HOLDING_COST_FACTOR)))) ** Decimal(0.5)

    # make another summary for as a dictionary and allow each value to be retrieved individually
    def orders_summary(self) -> dict:
        return {'sku': self.__sku_id, 'average_order': '{:.0f}'.format(self.__average_order),
                'standard_deviation': '{:.0f}'.format(self.__orders_standard_deviation),
                'safety_stock': '{:.0f}'.format(self.__safety_stock),
                'demand_variability': '{:.3f}'.format(self.__demand_variability),
                'reorder_level': '{:.0f}'.format(self.__reorder_level),
                'reorder_quantity': '{:.0f}'.format(self.__fixed_reorder_quantity),
                'revenue': '{:.2f}'.format(self.__sku_revenue),
                'economic_order_quantity': '{:.0f}'.format(self.__economic_order_qty),
                'economic_order_variable_cost': '{:.2f}'.format(self.__economic_order_variable_cost),
                'ABC_XYZ_Classification': '{0}{1}'.format(self.__abc_classification, self.__xyz_classification)}

    def orders_summary_simple(self) -> dict:
        return {'sku': self.__sku_id, 'average_order': '{:.0f}'.format(self.__average_order),
                'standard_deviation': '{:.0f}'.format(self.__orders_standard_deviation),
                'safety_stock': '{:.0f}'.format(self.__safety_stock),
                'demand_variability': '{:.3f}'.format(self.__demand_variability),
                'reorder_level': '{:.0f}'.format(self.__reorder_level),
                'reorder_quantity': '{:.0f}'.format(self.__fixed_reorder_quantity),
                'revenue': '{:.2f}'.format(self.__sku_revenue)}

    def __del__(self):

        self.__orders = None
        self.__sku_id = None
        self.__lead_time = None
        self.__unit_cost = None
        self.__z_value = None
        self.__count_orders = None
        self.__average_order = None
        self.__orders_standard_deviation = None
        self.__safety_stock = None
        self.__demand_variability = None
        self.__reorder_level = None
        self.__reorder_cost = None
        self.__fixed_reorder_quantity = None
        # class_name = self.__class__.__name__
        # print(class_name + " destroyed")
