from decimal import Decimal
from operator import attrgetter


# TODO-feature Allow user to set the boundaries for classe classification
class AbcXyz:
    '''Applies abc xyz analysis on a collection of demand passed into the '''

    __cumulative_total_revenue = Decimal(0)
    __percentage_revenue = Decimal(0)
    __a_class = "A"
    __b_class = "B"
    __c_class = "C"
    __x_class = "X"
    __y_class = "Y"
    __z_class = "Z"
    __abcxyz_summary = []

    def __init__(self, orders_collection: list):
        self.__orders = orders_collection
        self.__cumulative_total_revenue = self._cumulative_total()
        self.percentage_revenue()
        self.cumulative_percentage_revenue()
        self.abc_classification()
        self.xyz_classification()
        self.__abcxyz_summary = self.classification_summary()

    def __repr__(self):
        representation = "AX: {}, AY: {}, AZ: {} \nBX: {}, BY: {}, BZ: {}\nCX: {}, CY: {}, CZ: {}"
        return representation.format(len(self.__abcxyz_summary.get('AX')),
                                     len(self.__abcxyz_summary.get('AY')),
                                     len(self.__abcxyz_summary.get('AZ')),
                                     len(self.__abcxyz_summary.get('BX')),
                                     len(self.__abcxyz_summary.get('BY')),
                                     len(self.__abcxyz_summary.get('BZ')),
                                     len(self.__abcxyz_summary.get('CX')),
                                     len(self.__abcxyz_summary.get('CY')),
                                     len(self.__abcxyz_summary.get('CZ')))


    @property
    def ax(self):
        return self.__abcxyz_summary.get('AX')

    @property
    def ay(self):
        return self.__abcxyz_summary.get('AY')

    @property
    def az(self):
        return self.__abcxyz_summary.get('AZ')

    @property
    def bx(self):
        return self.__abcxyz_summary.get('BX')

    @property
    def by(self):
        return self.__abcxyz_summary.get('BY')

    @property
    def bz(self):
        return self.__abcxyz_summary.get('BZ')

    @property
    def cx(self):
        return self.__abcxyz_summary.get('CX')

    @property
    def cy(self):
        return self.__abcxyz_summary.get('CY')

    @property
    def cz(self):
        return self.__abcxyz_summary.get('CZ')


                    # @property
        # def orders(self)->list:
        #     return self.__orders

    # @orders.setter
    # def orders(self, orders):
    #    self.__orders = orders

    @property
    def abcxyz_summary(self) -> list:
        return self.__abcxyz_summary

    @abcxyz_summary.setter
    def abcxyz_summary(self, abcxyz):
        self.__abcxyz_summary = abcxyz

    def _cumulative_total(self) -> Decimal:
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

    def classification_summary(self):

        ax_count = [sku for sku in self.__orders if sku.abcxyz_classification == 'AX']

        ay_count = [sku for sku in self.__orders if sku.abcxyz_classification == 'AY']

        az_count = [sku for sku in self.__orders if sku.abcxyz_classification == 'AZ']

        bx_count = [sku for sku in self.__orders if sku.abcxyz_classification == 'BX']

        by_count = [sku for sku in self.__orders if sku.abcxyz_classification == 'BY']

        bz_count = [sku for sku in self.__orders if sku.abcxyz_classification == 'BZ']

        cx_count = [sku for sku in self.__orders if sku.abcxyz_classification == 'CX']

        cy_count = [sku for sku in self.__orders if sku.abcxyz_classification == 'CY']

        cz_count = [sku for sku in self.__orders if sku.abcxyz_classification == 'CZ']

        classification_matrix ={"AX": ax_count,
                                "AY": ay_count,
                                "AZ": az_count,
                                "BX": bx_count,
                                "BY": by_count,
                                "BZ": bz_count,
                                "CX": cx_count,
                                "CY": cy_count,
                                "CZ": cz_count}
        self.__orders = []
        return classification_matrix

        # ranking method returns the demand list of dictionaries back in order
