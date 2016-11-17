from decimal import Decimal


class Shortages:
    def __init__(self, unit_cost: Decimal, reorder_cost: Decimal, holding_cost: Decimal):
        self.__unit_cost = unit_cost
        self.__reorder_cost = reorder_cost
        self.__holding_cost = holding_cost

    @property
    def unit_cost(self) -> Decimal:
        return self.__unit_cost

    @unit_cost.setter
    def unit_cost(self, unit_cost:Decimal):
        self.__unit_cost = unit_cost

    @property
    def reorder_cost(self) -> Decimal:
        return self.__reorder_cost

    @reorder_cost.setter
    def reorder_cost(self, reorder_cost: Decimal):
        self.__reorder_cost = reorder_cost

    @property
    def holding_cost(self) ->Decimal:
        return self.__holding_cost

    @holding_cost.setter
    def holding_cost(self, holding_cost):
        self.__holding_cost = holding_cost

    def total_cost_per_cycle(self):
        pass

    def optimal_order_size(self):
        pass

    def optimal_back_order(self):
        pass
