from decimal import Decimal, getcontext, ROUND_HALF_UP
from supplychainpy.demand import analyse_uncertain_demand
from supplychainpy.demand.eoq import minimum_variable_cost, economic_order_quantity


class EconomicOrderQuantity(analyse_uncertain_demand.UncertainDemand):
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
        getcontext().prec = 2
        getcontext().rounding = ROUND_HALF_UP
        self.__reorder_quantity = Decimal(reorder_quantity)
        self.__holding_cost = holding_cost
        self.__reorder_cost = reorder_cost
        self.__unit_cost = unit_cost
        self.__min_variable_cost = minimum_variable_cost(total_orders, reorder_cost, unit_cost, holding_cost)
        self.__economic_order_quantity = economic_order_quantity(total_orders, reorder_cost, unit_cost,holding_cost, reorder_quantity)

    def _minimum_variable_cost(self, average_orders, reorder_cost, unit_cost) -> Decimal:
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
            # reorder cost * average demand all divided by order size + (demand size * holding cost)
            if counter < 1:
                order_size = self._order_size(average_orders=average_orders, reorder_cost=reorder_cost,
                                              unit_cost=unit_cost, holding_cost=holding_cost,
                                              order_factor=order_factor)

            vc = self._variable_cost(float(average_orders), float(reorder_cost), float(order_size), float(unit_cost), float(holding_cost))

            order_size += int(float(order_size) * step)
            if counter < 1:
                previous_eoq_variable_cost = Decimal(vc)

            while counter == 0:
                counter += 1
        return Decimal(previous_eoq_variable_cost)
        # probably missing the addition

    def _economic_order_quantity(self, average_orders: float, reorder_cost: float, unit_cost: float) -> Decimal:
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
            # reorder cost * average demand all divided by order size + (demand size * holding cost)
            if counter < 1:
                order_size = self._order_size(average_orders=average_orders, reorder_cost=reorder_cost,
                                              unit_cost=unit_cost, holding_cost=holding_cost,
                                              order_factor=order_factor)


            vc = self._variable_cost(float(average_orders), float(reorder_cost), float(order_size), float(unit_cost), float(holding_cost))

            order_size += int(float(order_size) * step)
            if counter < 1:
                previous_eoq_variable_cost = Decimal(vc)

            while counter == 0:
                counter += 1

        return Decimal(order_size)

    @staticmethod
    def _variable_cost(average_orders: float, reorder_cost: float, order_size: float, unit_cost: float,
                       holding_cost: float) -> float:

        rc = lambda x, y, z: (x * y) / z
        hc = lambda x, y, z: x * y * z
        vc = rc(float(average_orders), float(reorder_cost), float(order_size)) + hc(float(unit_cost),
                                                                                    float(order_size),
                                                                                    float(holding_cost))
        return vc

    @staticmethod
    def _order_size(average_orders: float, reorder_cost: float, unit_cost: float, holding_cost: float,
                    order_factor: float) -> float:

        order_size_calc = lambda x, y, z, i, j: int(
            (float(x) * float(y) * 2) / (float(z) * float(i)) * float(j) * float(0.5))

        order_size = order_size_calc(average_orders, reorder_cost, unit_cost, holding_cost, order_factor)

        return order_size
