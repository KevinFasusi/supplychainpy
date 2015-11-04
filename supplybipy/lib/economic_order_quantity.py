from decimal import Decimal


class EconomicOrderQuantity:
    __economic_order_quantity = Decimal(0)
    __reorder_cost = Decimal(0)
    __holding_cost = Decimal(0)
    __min_variable_cost = Decimal(0)
    __reorder_quantity = Decimal(0)

    @property
    def minimum_variable(self):
        return self.__min_variable_cost

    @property
    def economic_order_quantity(self):
        return self.__economic_order_quantity

    def __init__(self, reorder_quantity, holding_cost, reorder_cost, average_orders):
        self.__reorder_quantity = reorder_quantity
        self.__holding_cost = holding_cost
        self.__reorder_cost = reorder_cost
        self.__min_variable_cost = self._minimum_variable_cost(average_orders, reorder_cost)
        self.__economic_order_quantity = self._eoq_for_minimum_variable_cost(average_orders, reorder_cost)

    def _minimum_variable_cost(self, average_orders, reorder_cost):
        holding_cost = self.__holding_cost
        reorder_quantity = self.__reorder_quantity
        step = Decimal(1.2)
        previous_eoq_variable_cost = Decimal(0)
        eoq_variable_cost = Decimal(0)

        while previous_eoq_variable_cost <= eoq_variable_cost:
            # reorder cost * average demand all divided by order size + (orders size * holding cost)
            previous_eoq_variable_cost = Decimal(eoq_variable_cost)
            eoq_variable_cost = ((Decimal(average_orders) * Decimal(reorder_cost)) / reorder_quantity) + (
                Decimal(reorder_quantity) * Decimal(Decimal(holding_cost) * Decimal(reorder_quantity)))
            reorder_quantity *= step
        return Decimal(previous_eoq_variable_cost)
        # probabaly missing the addition

    def _eoq_for_minimum_variable_cost(self, average_orders, reorder_cost):
        holding_cost = self.__holding_cost
        reorder_quantity = self.__reorder_quantity
        step = Decimal(1.2)
        previous_eoq_variable_cost = Decimal(0)
        eoq_variable_cost = Decimal(0)

        while previous_eoq_variable_cost <= eoq_variable_cost:
            # reorder cost * average demand all divided by order size + (orders size * holding cost)
            previous_eoq_variable_cost = Decimal(eoq_variable_cost)
            eoq_variable_cost = ((Decimal(average_orders) * Decimal(reorder_cost)) / reorder_quantity) + (
                Decimal(reorder_quantity) * Decimal(Decimal(holding_cost) * Decimal(reorder_quantity)))
            reorder_quantity *= step
        return Decimal(reorder_quantity)
