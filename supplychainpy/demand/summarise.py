from operator import attrgetter

from decimal import Decimal

from supplychainpy.demand.abc_xyz import AbcXyz


class OrdersAnalysis:
    def __init__(self, analysed_orders: list):
        self.__analysed_orders = analysed_orders
        self.__abc_xyz = self._abc_xyz_summary_raw()

    @property
    def abc_xyz_raw(self):
        return self.__abc_xyz

    def top_sku(self, attribute: str, count: int, reverse: bool = True) -> dict:

        try:
            for index, sku in enumerate(sorted(self.__analysed_orders, key=attrgetter(attribute), reverse=reverse)):
                if index > count:
                    break
                yield sku.orders_summary()
        except AttributeError as e:
            possible_attributes = "Incorrect attribute provided as key. Please use one of the following:\n" \
                                  "demand_variability\neconomic_order_quantity\naverage_order\nsafety_stock" \
                                  "\nstandard_deviation\nreorder_level\nreorder_quantity\nrevenue\n" \
                                  "economic_order_quantity\neconomic_order_variable_cost\n" \
                                  "ABC_XYZ_Classification'\nexcess_stock\nshortages"
            print(possible_attributes)

    def _abc_xyz_summary_raw(self):
        abc = AbcXyz(self.__analysed_orders)
        abc.classification_summary()
        # return total excess, shortages,
        return abc

    def abc_xyz_summary(self, classification: list = ('AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ'),
                        category: list = ('excess_stock', 'shortages', 'revenue'), value: str = 'currency') -> dict:
        """Retrieve currency value or units for key metrics by classification"""

        # Retrieves a subset of the orders analysis based on the classification (AX, AY, AZ...) held in dict
        filtered_summary = []
        temp_sum = 0.0
        style = {'AX': [analysis if self.__abc_xyz.ax is not None else 0 for analysis in self.__abc_xyz.ax],
                 'AY': [analysis if self.__abc_xyz.ay is not None else 0 for analysis in self.__abc_xyz.ay],
                 'AZ': [analysis if self.__abc_xyz.az is not None else 0 for analysis in self.__abc_xyz.az],
                 'BX': [analysis if self.__abc_xyz.bx is not None else 0 for analysis in self.__abc_xyz.bx],
                 'BY': [analysis if self.__abc_xyz.by is not None else 0 for analysis in self.__abc_xyz.by],
                 'BZ': [analysis if self.__abc_xyz.bz is not None else 0 for analysis in self.__abc_xyz.bz],
                 'CX': [analysis if self.__abc_xyz.cx is not None else 0 for analysis in self.__abc_xyz.cx],
                 'CY': [analysis if self.__abc_xyz.cy is not None else 0 for analysis in self.__abc_xyz.cy],
                 'CZ': [analysis if self.__abc_xyz.cz is not None else 0 for analysis in self.__abc_xyz.cz]}
        try:
            # filters the subset based on classification and category requested and return the currency vale of the
            t = {}
            temp_sum = Decimal(0)
            unit_cost = Decimal(0)
            for id in classification:
                for label in category:
                    summary = style.get(id)
                    for k in summary:
                        unit_cost = k.unit_cost
                        t = {**k.orders_summary()}
                        temp_sum += Decimal(t.get(label))
                    if label == 'revenue':
                        filtered_summary.append({id: {label: float(temp_sum)}})
                    elif label != 'revenue' and value == 'currency':
                        filtered_summary.append({id: {'{}_cost'.format(label): float(temp_sum * unit_cost)}})
                    else:
                        filtered_summary.append({id: {'{}_cost'.format(label): float(temp_sum)}})
                    temp_sum = 0
            return filtered_summary
        except AttributeError as e:
            print("Incorrect Category or Attribute empty. Please ")
