from decimal import Decimal
from operator import attrgetter


# TODO-feature Allow user to set the boundaries for classe classification
class AbcXyz:
    '''Applies abc xyz analysis on a collection of demand passed into the '''
    __orders = {}
    __cumulative_total_revenue = Decimal(0)
    __percentage_revenue = Decimal(0)
    __a_class = "A"
    __b_class = "B"
    __c_class = "C"
    __x_class = "X"
    __y_class = "Y"
    __z_class = "Z"
    __abcxyz_summary = []

    def __init__(self, orders_collection):
        self.__orders = orders_collection
        self.__cumulative_total_revenue = self._cumulative_total()

    @property
    def orders(self):
        return self.__orders

    @orders.setter
    def orders(self, orders):
        self.__orders = orders

    @property
    def abcxyz_summary(self):
        return self.__abcxyz_summary

    @abcxyz_summary.setter
    def abcxyz_summary(self, abcxyz):
        self.__abcxyz_summary = abcxyz

    def _cumulative_total(self):
        cumulative_total = Decimal(0)
        for sku in self.__orders:
            cumulative_total += Decimal(sku.revenue)
        return cumulative_total

    def percentage_revenue(self):
        for sku in self.__orders:
            sku.percentage_revenue = Decimal(sku.revenue) / Decimal(self.__cumulative_total_revenue)

    def cumulative_percentage_revenue(self):
        previous_total = Decimal(0)
        for sku in sorted(self.__orders, key=attrgetter('revenue'), reverse=True):
            sku.cumulative_percentage = Decimal(sku.percentage_revenue) + previous_total
            previous_total = sku.percentage_revenue + previous_total

    def abc_classification(self):
        for sku in sorted(self.__orders, key=attrgetter('revenue'), reverse=True):
            if sku.cumulative_percentage <= .80:
                sku.abc_classification = self.__a_class
            elif .80 < sku.cumulative_percentage <= .90:
                sku.abc_classification = self.__b_class
            else:
                sku.abc_classification = self.__c_class

    def xyz_classification(self):
        for sku in self.__orders:
            if sku.demand_variability <= Decimal(0.20):
                sku.xyz_classification = self.__x_class
            elif Decimal(0.20) < sku.demand_variability <= Decimal(0.60):
                sku.xyz_classification = self.__y_class
            else:
                sku.xyz_classification = self.__z_class

# ranking method returns the demand list of dictionaries back in order
