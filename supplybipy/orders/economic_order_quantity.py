from decimal import Decimal, getcontext, ROUND_HALF_UP
from . import analyse_orders


class EconomicOrderQuantity(analyse_orders.OrdersUncertainDemand):
    __economic_order_quantity = Decimal(0)
    analyse_orders.OrdersUncertainDemand.__reorder_cost = Decimal(0)
    __holding_cost = Decimal(0)
    __min_variable_cost = Decimal(0)
    __reorder_quantity = Decimal(0)
    __unit_cost = 0.00

    @property
    def minimum_variable_cost(self):
        return self.__min_variable_cost

    @property
    def economic_order_quantity(self):
        return self.__economic_order_quantity

    def __init__(self, reorder_quantity, holding_cost, reorder_cost, average_orders, unit_cost):
        getcontext().prec = 2
        getcontext().rounding = ROUND_HALF_UP
        self.__reorder_quantity = Decimal(reorder_quantity)
        self.__holding_cost = holding_cost
        self.__reorder_cost = reorder_cost
        self.__unit_cost = unit_cost
        self.__min_variable_cost = self._minimum_variable_cost(average_orders, reorder_cost, unit_cost)
        self.__economic_order_quantity = self._eoq_for_minimum_variable_cost(average_orders, reorder_cost, unit_cost)

    def _minimum_variable_cost(self, average_orders, reorder_cost, unit_cost):
        getcontext().prec = 2
        getcontext().rounding = ROUND_HALF_UP
        holding_cost = self.__holding_cost

        step = float(0.2)
        previous_eoq_variable_cost = Decimal(0)

        Decimal(reorder_cost)
        order_factor = float(0.002)
        vc = 0.00
        counter = 0
        order_size = 0
        while previous_eoq_variable_cost >= Decimal(vc):

            previous_eoq_variable_cost = Decimal(vc)
            # reorder cost * average demand all divided by order size + (orders size * holding cost)
            if counter < 1:
                order_size = int((float(average_orders) * float(reorder_cost) * 2) / (
                    float(unit_cost) * float(holding_cost)) * order_factor) * float(0.5)

            else:
                pass

            rc = Decimal((float(average_orders) * float(reorder_cost)) / float(order_size))
            hc = Decimal((float(unit_cost) * float(order_size)) * float(holding_cost))
            vc = Decimal(float(rc) + float(hc))
            order_size += int(float(order_size) * step)
            if counter < 1:
                previous_eoq_variable_cost = Decimal(vc)
            else:
                pass

            while counter == 0:
                counter += 1
        return Decimal(previous_eoq_variable_cost)
        # probabaly missing the addition

    def _eoq_for_minimum_variable_cost(self, average_orders, reorder_cost, unit_cost):
        getcontext().prec = 2
        getcontext().rounding = ROUND_HALF_UP
        holding_cost = self.__holding_cost
        reorder_quantity = int(self.__reorder_quantity)
        step = float(0.2)
        previous_eoq_variable_cost = Decimal(0)
        eoq_variable_cost = Decimal(0)
        Decimal(reorder_cost)
        order_factor = float(0.002)
        vc = 0.00
        rc = 0.00
        hc = 0.00
        s = 0.00
        counter = 0
        order_size = 0
        diff = Decimal(0)
        while previous_eoq_variable_cost >= Decimal(vc):

            previous_eoq_variable_cost = Decimal(vc)
            # reorder cost * average demand all divided by order size + (orders size * holding cost)
            if counter < 1:
                order_size = int((float(average_orders) * float(reorder_cost) * 2) / (
                    float(unit_cost) * float(holding_cost)) * order_factor) * float(0.5)

            else:
                pass

            rc = Decimal((float(average_orders) * float(reorder_cost)) / float(order_size))
            hc = Decimal((float(unit_cost) * float(order_size)) * float(holding_cost))
            vc = Decimal(float(rc) + float(hc))
            order_size += int(float(order_size) * step)
            if counter < 1:
                previous_eoq_variable_cost = Decimal(vc)
            else:
                pass

            while counter == 0:
                counter += 1

        return Decimal(order_size)
