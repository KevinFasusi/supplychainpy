from math import sqrt
from decimal import *


class OrdersUncertainDemand:
    __sku_id = ""
    __average_order = Decimal(0)
    __count_orders = 0
    __orders = {}
    __orders_standard_deviation = Decimal(0)
    __z_value = 0.00  # default set to 90%
    __lead_time = 0
    __safety_stock = 0
    __demand_variability = Decimal(0)
    __reorder_level = 0
    __unit_cost = 0.00
    __reorder_cost = 0.00
    __CONST_HOLDING_COST_FACTOR = Decimal(0.25)
    __fixed_reorder_quantity = 0

    def __init__(self, orders, sku, lead_time, unit_cost, reorder_cost, z_value=Decimal(1.28)):
        # need to check all orders entered are integers

        self.__orders = orders
        self.__sku_id = sku
        self.__lead_time = Decimal(lead_time)
        self.__unit_cost = Decimal(unit_cost)
        self.__z_value = z_value
        self.__count_orders = len(self.__orders.values())
        if len(orders) < 2:
            self.__average_order = Decimal(self.average_order_row())
            self.__orders_standard_deviation = self._standard_deviation_orders_row()
        else:
            self.__average_order = Decimal(self.average_order)
            self.__orders_standard_deviation = self._standard_deviation_orders()
        self.__safety_stock = self._safety_stock()
        self.__demand_variability = self._demand_variability()
        self.__reorder_level = Decimal(self._reorder_level())
        self.__reorder_cost = Decimal(reorder_cost)
        self.__fixed_reorder_quantity = Decimal(self._fixed_order_quantity())

    def __str__(self):
        return 'Orders analysis for uncertainty demand: SKU {} | Safety Stock {:.0f}'.format(self.__sku_id,
                                                                                             self.__safety_stock)

    def __repr__(self):
        return 'Orders analysis for uncertainty demand: SKU {} | Safety Stock {}'

    @property
    def order(self):
        return list(self.__orders.value)

    @order.setter
    def order(self, orders):
        self.__orders = orders

    def get_sku_id(self):
        return self.__sku_id

    def set_sku_id(self, sku):
        self.__sku_id = sku

    @property
    def lead_time(self):
        return self.__lead_time

    @lead_time.setter
    def lead_time(self, lead_time):
        self.__lead_time = lead_time

    def get_average_orders(self):
        return self.__average_order

    def get_sku_id(self):
        return self.__sku_id

    def set_sku_id(self, sku_id):
        self.__sku_id = sku_id

    @property
    def average_order(self):
        return float(sum(self.__orders.values()) / self.__count_orders)

    def average_order_row(self):
        total_orders = 0
        for item in self.__orders:
            orders_list = self.__orders[item]
        for item in orders_list:
            total_orders += Decimal(item)
        return Decimal(total_orders / len(orders_list))

    def _standard_deviation_orders(self, variance=[], deviation=0):
        for x in self.__orders.values():
            variance.append(Decimal(x - self.__average_order))
        for j in variance:
            deviation += Decimal(j) ** Decimal(2)
        deviation /= Decimal(self.__count_orders)
        return round(deviation ** Decimal(0.5), 1)

    def _standard_deviation_orders_row(self, variance=[], deviation=0):
        for item in self.__orders:
            orders_list = self.__orders[item]
        for item in orders_list:
            variance.append(Decimal(Decimal(item) - self.__average_order))
        for j in variance:
            deviation += Decimal(j) ** Decimal(2)
        deviation /= Decimal(len(orders_list))
        return round(deviation ** Decimal(0.5), 1)

    def _safety_stock(self):
        return Decimal(self.__z_value) * Decimal(self.__orders_standard_deviation) * Decimal(
            (self.__lead_time ** Decimal(0.5)))

    def _demand_variability(self):
        return self.__orders_standard_deviation / Decimal(self.__average_order)

    def _reorder_level(self):
        return round(
            (Decimal(self.__lead_time ** Decimal(0.5)) * Decimal(self.__average_order)) + Decimal(self.__safety_stock))

    # provide the facility to output order quantity as a range if the reorder cost is an estimation
    # one version when holding cost has not been specified and one when it has been

    def _fixed_order_quantity(self):
        return (2 * Decimal(self.__reorder_cost) * (
            self.__average_order / (self.__unit_cost * self.__CONST_HOLDING_COST_FACTOR))) ** Decimal(0.5)

    # make another summary for as a dictionary and allow each value to be retrieved individually

    def orders_summary(self):
        return {'sku': self.__sku_id, 'average order': '{:.0f}'.format(self.__average_order),
                'standard deviation': '{:.0f}'.format(self.__orders_standard_deviation),
                'safety stock': '{:.0f}'.format(self.__safety_stock),
                'demand variability': '{:.3f}'.format(self.__demand_variability),
                'reorder level': '{}'.format(self.__reorder_level),
                'reorder quantity': '{:.0f}'.format(self.__fixed_reorder_quantity)}

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
        print("deleted")
