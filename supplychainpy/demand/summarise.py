from collections import ChainMap
from operator import attrgetter

from decimal import Decimal
import numpy as np
from supplychainpy.demand.abc_xyz import AbcXyz
from supplychainpy.demand.analyse_uncertain_demand import UncertainDemand


class OrdersAnalysis:
    def __init__(self, analysed_orders: list):
        self.__analysed_orders = analysed_orders
        self.__abc_xyz = self._abc_xyz_summary_raw()

    @property
    def abc_xyz_raw(self):
        return self.__abc_xyz

    def top_sku(self, attribute: str, count: int = 0, reverse: bool = True) -> dict:
        if count == 0:
            count = len(self.__analysed_orders)

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

        except TypeError as e:
            print("Failed {}".format(e))

    def _abc_xyz_summary_raw(self):
        abc = AbcXyz(self.__analysed_orders)
        abc.classification_summary()
        # return total excess, shortages,
        return abc

    def abc_xyz_summary(self, classification: list = ('AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ'),
                        category: list = ('excess_stock', 'shortages', 'revenue'), value: str = 'currency') -> dict:
        """Retrieve currency value or units for key metrics by classification"""

        # Retrieves a subset of the orders analysis based on the classification (AX, AY, AZ...) held in dict

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
            temp_sum = Decimal(0)
            unit_cost = Decimal(0)

            temp_currency_summary = {}

            for id in classification:
                for label in category:
                    summary = style.get(id)
                    for sku in summary:
                        unit_cost = sku.unit_cost
                        t = {**sku.orders_summary()}
                        temp_sum += Decimal(t.get(label))
                        t.clear()

                    if label == 'revenue':
                        temp_currency_summary.update({label: float(temp_sum)})

                    elif label != 'revenue' and value == 'currency':
                        temp_currency_summary.update({'{}_cost'.format(label): float(temp_sum * unit_cost)})

                    else:
                        temp_currency_summary.update({'{}_cost'.format(label): float(temp_sum)})

                    temp_sum = 0

                yield {id: temp_currency_summary}
                temp_currency_summary.clear()

        except AttributeError as e:
            print("Incorrect Category or Attribute empty. {}".format(e))

    def describe_sku(self, *args):
        summary = []
        for arg in args:
            summary.append(self._summarise_sku(arg))
        yield summary

    def _summarise_sku(self, sku_id: str):
        selection = UncertainDemand

        for sku in self.__analysed_orders:
            if sku.sku_id == sku_id:
                selection = sku
                break

        # TODO-fix fix problem with min and max values
        summary = {'sku_id': '{}'.format(selection.sku_id),
                   'revenue_rank': '{}'.format(self._rank(sku_id=sku_id, attribute='revenue')),
                   'revenue': '{}'.format(selection.revenue),
                   'retail_price': '{}'.format(selection.retail_price),
                   'gross_profit_margin': '{}'.format(Decimal(selection.retail_price) - selection.unit_cost),
                   'markup_percentage': '{}'.format((Decimal(selection.retail_price) - selection.unit_cost) / selection.unit_cost),
                   'unit_cost': '{}'.format(selection.unit_cost),
                   'excess_rank': '{}'.format(self._rank(sku_id=sku_id, attribute='excess_stock_cost')),
                   'excess_units': '{}'.format(selection.excess_stock),
                   'excess_cost': '{}'.format(Decimal(selection.excess_stock_cost)),
                   'shortage_rank': '{}'.format(self._rank(sku_id=sku_id, attribute='shortage_cost')),
                   'shortage_units': '{}'.format(selection.shortages),
                   'shortage_cost': '{}'.format(selection.shortage_cost),
                   'safety_stock_units': '{}'.format(selection.safety_stock),
                   'safety_stock_cost': '{}'.format(selection.safety_stock_cost),
                   'safety_stock_rank': '{}'.format(self._rank(sku_id=sku_id, attribute='safety_stock_cost')),
                   'classification': '{}'.format(selection.abcxyz_classification),
                   'average_orders': '{}'.format(selection.average_orders),
                   'min_order': '{}'.format(min(map(int,selection.orders))),
                   'max_order': '{}'.format(max(map(int,selection.orders))),
                   'percentage_contribution_revenue': '{}'.format(selection.percentage_revenue)
                   }
        return summary

    def _rank(self, sku_id, attribute):
        for index, t in enumerate(sorted(self.__analysed_orders, key=attrgetter(attribute), reverse=True)):
            if t.sku_id == sku_id:
                return index + 1
