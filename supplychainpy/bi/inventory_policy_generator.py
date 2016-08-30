from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand
from string import Template


class PolicyGenerator:
    #def __init__(self, analysed_orders: UncertainDemand):
    #    self._analysed_orders = analysed_orders

    def templates(self):
        safety_stock = {'high': Template('$sku $status $ ')}


if __name__ == '__main__':
    d = PolicyGenerator()

