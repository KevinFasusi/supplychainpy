from decimal import Decimal, getcontext, ROUND_HALF_UP

import pyximport

from supplychainpy.inventory import analyse_uncertain_demand

pyximport.install()
from supplychainpy.inventory.eoq import minimum_variable_cost
from supplychainpy.inventory.eoq import economic_order_quantity


class EconomicOrderQuantity:
    __economic_order_quantity = Decimal(0)
    analyse_uncertain_demand.UncertainDemand.__reorder_cost = Decimal(0)
    __holding_cost = Decimal(0)
    __min_variable_cost = Decimal(0)
    __reorder_quantity = Decimal(0)
    __unit_cost = 0.00

    @property
    def minimum_variable_cost(self) -> Decimal:
        return self.__min_variable_cost

    @property
    def economic_order_quantity(self) -> Decimal:
        return self.__economic_order_quantity

    def __init__(self, reorder_quantity: float, holding_cost: float, reorder_cost: float, average_orders: float,
                 unit_cost: float, total_orders: float):
        getcontext().prec = 8
        getcontext().rounding = ROUND_HALF_UP
        self.__reorder_quantity = Decimal(reorder_quantity)
        self.__holding_cost = holding_cost
        self.__reorder_cost = reorder_cost
        self.__unit_cost = unit_cost
        self.__min_variable_cost = minimum_variable_cost(total_orders, reorder_cost, unit_cost, holding_cost)
        self.__economic_order_quantity = economic_order_quantity(total_orders, reorder_cost, unit_cost, holding_cost,
                                                                 reorder_quantity)


