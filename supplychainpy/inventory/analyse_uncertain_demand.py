# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import itertools
import logging
from collections import Iterable
from decimal import Decimal
from decimal import getcontext

from supplychainpy._helpers._decorators import log_this
from supplychainpy._helpers._enum_formats import PeriodFormats
from supplychainpy.model_demand import holts_trend_corrected_exponential_smoothing_forecast
from supplychainpy.model_demand import simple_exponential_smoothing_forecast


def _standard_deviation_orders(orders: dict, average_order: Decimal) -> Decimal:
    deviation = Decimal(0)
    variance = []
    for x in orders.values():
        variance.append(Decimal(x - average_order))
    for j in variance:
        deviation += Decimal(j) ** Decimal(2)
    deviation /= Decimal(len(variance))
    return Decimal(Decimal(deviation) ** Decimal(0.5))


# TODO-feature convert orders data into correct period
# TODO-feature convert list of lead-times to average lead-times

class UncertainDemand:
    """ Models inventory profile calculating economic order quantity, variable cost, reorder quantity and
        ABCXYZ classification
    """
    __z_value = Decimal(0.00)  # default set to 90%
    __lead_time = 0
    __safety_stock = 0
    __demand_variability = Decimal(0)
    __reorder_level = 0
    __unit_cost = Decimal(0.00)
    __reorder_cost = Decimal(00.00)
    __CONST_HOLDING_COST_FACTOR = Decimal(0.25)
    __fixed_reorder_quantity = 0
    __DAYS = Decimal(7)
    __WEEKS = Decimal(4)
    __MONTHS = Decimal(12)
    __QUARTER = Decimal(4)
    __period = 0
    __sku_revenue = Decimal(0)
    __percentage_of_revenue = Decimal(0)
    __cumulative_percentage = Decimal(0)
    __abc_classification = ""
    __xyz_classification = ""
    __economic_order_variable_cost = Decimal(0)
    __economic_order_qty = Decimal(0)
    getcontext().prec = 8
    _summary_keywords = ['sku', 'standard_deviation', 'safety_stock', 'demand_variability', 'reorder_level',
                         'reorder_quantity', 'revenue', 'economic_order_quantity', 'economic_order_variable_cost',
                         'ABC_XYZ_Classification', 'excess_stock', 'shortages', 'average_orders', 'unit_cost',
                         'quantity_on_hand', 'currency', 'orders', 'total_orders', 'backlog']
    __rank = 0

    def __init__(self, orders: dict, sku: str, currency: str, lead_time: Decimal, unit_cost: Decimal,
                 reorder_cost: Decimal,
                 z_value: Decimal = Decimal(1.28), holding_cost: Decimal = 0.00, retail_price: Decimal = 0.00,
                 period: str = PeriodFormats.months.name, quantity_on_hand: Decimal = 0.00, backlog: Decimal = 0.00):
        self.__currency = currency
        self.__orders = orders
        self.__sku_id = sku
        self.__lead_time = Decimal(lead_time)
        self.__unit_cost = Decimal(unit_cost)
        self.__retail_price = Decimal(retail_price)
        self.__quantity_on_hand = Decimal(quantity_on_hand)
        self.__z_value = z_value
        self.__count_orders = len(self.__orders)

        if len(orders) < 2:
            self.__average_order = Decimal(self.average_order_row())
            self.__orders_standard_deviation = self._standard_deviation_orders_row()
        else:
            self.__average_order = Decimal(self.average_order())
            self.__orders_standard_deviation = _standard_deviation_orders(orders=orders,
                                                                          average_order=self.__average_order)
        self.__sku_revenue = self._revenue(orders=orders)
        self.__safety_stock = self._safety_stock()
        self.__demand_variability = self._demand_variability()
        self.__reorder_level = Decimal(self._reorder_level())
        self.__reorder_cost = Decimal(reorder_cost)
        self.__fixed_reorder_quantity = Decimal(self._fixed_order_quantity())
        self.__period = period
        self.__excess_stock = self._excess_qty()
        self.__backlog = Decimal(backlog)
        self.__shortage_qty = self._shortage_qty()
        self.__total_orders = self._sum_orders()


    @property
    def backlog(self) -> Decimal:
        return self.__backlog

    @property
    def simple_exponential_smoothing_forecast(self):
        return self._generate_optimised_ses_forecast()

    @property
    def holts_trend_corrected_forecast(self):
        return self._generate_holts_es_forecast()

    @property
    def total_orders(self):
        return self.__total_orders

    @property
    def currency(self):
        return self.__currency

    @property
    def quantity_on_hand(self):
        return self.__quantity_on_hand

    @property
    def excess_stock_cost(self):
        return self.__excess_stock * self.__unit_cost

    @property
    def shortage_cost(self):
        return self.__shortage_qty * self.__unit_cost

    @property
    def safety_stock_cost(self):
        return self.__safety_stock * self.__unit_cost

    @property
    def retail_price(self):
        return self.__retail_price

    @retail_price.setter
    def retail_price(self, retail_price):
        self.__retail_price = retail_price

    @property
    def excess_stock(self):
        return self.__excess_stock

    @excess_stock.setter
    def excess_stock(self, excess):
        self.__excess_stock = excess

    @property
    def shortages(self):
        return self.__shortage_qty

    @shortages.setter
    def shortages(self, shortage):
        self.__shortage_qty = shortage

    @property
    def safety_stock(self):
        return self.__safety_stock

    @safety_stock.setter
    def safety_stock(self, safety_stock):
        self.__safety_stock = safety_stock

    @property
    def reorder_level(self):
        return self.__reorder_level

    @reorder_level.setter
    def reorder_level(self, reorder_level):
        self.__reorder_level = reorder_level

    @property
    def unit_cost(self) -> Decimal:
        return self.__unit_cost

    @unit_cost.setter
    def unit_cost(self, unit_cost):
        self.__unit_cost = unit_cost

    @property
    def abcxyz_classification(self) -> str:
        """Gets ABCXYZ classification as a concatenated string"""
        return self.__abc_classification + self.__xyz_classification

    @property
    def abc_classification(self) -> str:
        return self.__abc_classification

    @abc_classification.setter
    def abc_classification(self, abc_classifier: str):
        self.__abc_classification = abc_classifier

    @property
    def xyz_classification(self) -> str:
        return self.__xyz_classification

    @xyz_classification.setter
    def xyz_classification(self, xyz_classifier: str):
        self.__xyz_classification = xyz_classifier

    @property
    def percentage_revenue(self) -> Decimal:
        return self.__percentage_of_revenue

    @percentage_revenue.setter
    def percentage_revenue(self, percentage_orders):
        self.__percentage_of_revenue = percentage_orders

    @property
    def cumulative_percentage(self) -> Decimal:
        return self.__cumulative_percentage

    @cumulative_percentage.setter
    def cumulative_percentage(self, percentage_orders):
        self.__cumulative_percentage = percentage_orders

    @property
    def orders(self):
        return self.__orders.get("demand")

    @property
    def order(self):
        total_order = 0
        orders_list = []
        for items in self.__orders:
            orders_list = self.__orders[items]
        if isinstance(orders_list, Iterable):
            for item in orders_list:
                total_order += Decimal(item)
        else:
            for item in self.__orders:
                total_order += self.__orders[item]
        return total_order

    @property
    def order_count(self):
        return self.__count_orders

    @order.setter
    def order(self, orders):
        self.__orders = orders

    @property
    def sku_id(self):
        return self.__sku_id

    @sku_id.setter
    def sku_id(self, sku):
        self.__sku_id = sku

    @property
    def lead_time(self):
        return self.__lead_time

    @lead_time.setter
    def lead_time(self, lead_time):
        self.__lead_time = lead_time

    @property
    def average_orders(self):
        return self.__average_order

    @property
    def standard_deviation(self):
        return self.__orders_standard_deviation

    @property
    def revenue(self) -> Decimal:
        return self.__sku_revenue

    @property
    def demand_variability(self) -> Decimal:
        return self._demand_variability()

    @demand_variability.setter
    def demand_variability(self, demand_variability: Decimal):
        self.__demand_variability = demand_variability

    @property
    def fixed_order_quantity(self):
        return self.__fixed_reorder_quantity

    @fixed_order_quantity.setter
    def fixed_order_quantity(self, order):
        self.__fixed_reorder_quantity = order

    @property
    def economic_order_qty(self):
        return self.__economic_order_qty

    @economic_order_qty.setter
    def economic_order_qty(self, eoq):
        self.__economic_order_qty = eoq

    @property
    def economic_order_variable_cost(self) -> Decimal:
        return self.__economic_order_variable_cost

    @economic_order_variable_cost.setter
    def economic_order_variable_cost(self, eoq_vc):
        self.__economic_order_variable_cost = eoq_vc

    def average_order(self):
        return float(sum(self.__orders.values()) / self.__count_orders)

    def _sum_orders(self) -> int:
        total_orders = 0
        orders_list = []
        for item in self.__orders:
            if isinstance(self.__orders[item], Iterable):
                orders_list = self.__orders[item]
            else:
                orders_list.append(self.__orders[item])

        total_orders = sum([Decimal(item) for item in orders_list])
        return total_orders

    def average_order_row(self) -> Decimal:
        total_orders = 0
        orders_list = []
        for item in self.__orders:
            orders_list = self.__orders[item]
        for item in orders_list:
            total_orders += Decimal(item)
        return Decimal(total_orders / len(orders_list))

    def _revenue(self, orders: dict) -> Decimal:
        orders_list = []
        total_order = 0
        for items in orders:
            orders_list = orders[items]
        if isinstance(orders_list, Iterable):
            for item in orders_list:
                total_order += Decimal(item)
        else:
            for item in orders:
                total_order += orders[item]

        return Decimal(total_order * Decimal(self.__retail_price))

    def _standard_deviation_orders_row(self) -> Decimal:
        getcontext().prec = 12
        deviation = Decimal(0)
        variance = []
        orders_list = []
        for item in self.__orders:
            orders_list = self.__orders[item]
        for item in orders_list:
            variance.append(Decimal(Decimal(item) - Decimal(self.__average_order)))
        for j in variance:
            deviation += Decimal(j) ** Decimal(2)
        deviation /= Decimal(len(variance))
        return Decimal(Decimal(deviation) ** Decimal(0.5))

    # TODO-feature convert lead-time to correct period (data_set period must match lead_time priod if not conversion)
    def _safety_stock(self) -> Decimal:
        return Decimal(self.__z_value) * Decimal(self.__orders_standard_deviation) * Decimal(
            (self.__lead_time ** Decimal(0.5)))

    def _demand_variability(self) -> Decimal:
        return Decimal(Decimal(self.__orders_standard_deviation) / Decimal(self.__average_order))

    def _reorder_level(self) -> Decimal:
        return (Decimal(self.__lead_time ** Decimal(0.5)) * Decimal(self.__average_order)) + Decimal(
            self.__safety_stock)

    # provide the facility to output order quantity as a range if the reorder cost is an estimation
    # one version when holding cost has not been specified and one when it has been
    def _fixed_order_quantity(self) -> Decimal:
        return (2 * Decimal(self.__reorder_cost) * (
            Decimal(self.__average_order) / (
                Decimal(self.__unit_cost) * Decimal(self.__CONST_HOLDING_COST_FACTOR)))) ** Decimal(0.5)

    def _shortage_qty(self):
        if self.__quantity_on_hand < self.__safety_stock:
            return round(
                abs(((self.__reorder_level + (
                    self.__reorder_level - self.__safety_stock)) - self.__quantity_on_hand) + self.__backlog))
        else:
            return 0

    def _excess_qty(self):
        if self.__quantity_on_hand > self.__reorder_level + (self.__reorder_level - self.__safety_stock):
            return round(
                self.__quantity_on_hand - (self.__reorder_level + (self.__reorder_level - self.__safety_stock)), 0)
        else:
            return 0

    @log_this(logging.CRITICAL, message='Called to generate optimised SES forecast.')
    def _generate_optimised_ses_forecast(self):
        try:
            demand = (list(self.__orders.get("demand")))
            orders = [int(i) for i in demand]
            # filter for lowest standard order and use for evo model
            ses_evo_forecast = simple_exponential_smoothing_forecast(demand=orders, smoothing_level_constant=0.5,
                                                                     optimise=True)

            return ses_evo_forecast

        except TypeError as e:
            print('Exponential smoothing forecast (evolutionary model) failed. {}'.format(e))

    @log_this(logging.CRITICAL, message='Called to generate optimised HTCES forecast.')
    def _generate_holts_es_forecast(self):
        demand = (list(self.__orders.get("demand")))
        orders = [int(i) for i in demand]

        htces = holts_trend_corrected_exponential_smoothing_forecast(demand=orders, alpha=0.5, gamma=0.5, optimise=True)

        return htces

    def _summary(self, keywords: list) -> dict:
        pre_build = {'sku': self.__sku_id, 'average_order': '{:.0f}'.format(self.__average_order),
                     'standard_deviation': '{:.0f}'.format(self.__orders_standard_deviation),
                     'safety_stock': '{:.0f}'.format(self.__safety_stock),
                     'demand_variability': '{:.3f}'.format(self.__demand_variability),
                     'reorder_level': '{:.0f}'.format(self.__reorder_level),
                     'reorder_quantity': '{:.0f}'.format(self.__fixed_reorder_quantity),
                     'revenue': '{}'.format(self.__sku_revenue),
                     'economic_order_quantity': '{:.0f}'.format(self.__economic_order_qty),
                     'economic_order_variable_cost': '{:.2f}'.format(self.__economic_order_variable_cost),
                     'ABC_XYZ_Classification': '{0}{1}'.format(self.__abc_classification, self.__xyz_classification),
                     'excess_stock': '{}'.format(self.__excess_stock),
                     'shortages': '{}'.format(self.__shortage_qty),
                     'average_orders': '{}'.format(self.__average_order),
                     'unit_cost': '{}'.format(self.__unit_cost),
                     'quantity_on_hand': '{}'.format(self.__quantity_on_hand),
                     'currency': '{}'.format(self.__currency),
                     'orders': self.__orders,
                     'total_orders': '{}'.format(self.__total_orders),
                     'backlog': '{}'.format(self.__backlog)}
        summary = {}
        for key in keywords:
            summary.update({key: pre_build.get(key)})
        return summary

    def orders_summary(self) -> dict:
        return self._summary(self._summary_keywords)

    def orders_summary_simple(self) -> dict:
        return self._summary(
            itertools.chain(self._summary_keywords[:7], self._summary_keywords[9:len(self._summary_keywords)]))

    def __repr__(self):
        representation = "(sku_id: {}, average_order: {:.0f}, standard_deviation: {:.0f}, safety_stock: {:0f}, \n" \
                         "demand_variability: {:.3f}, reorder_level: {:.0f}, reorder_quantity: {:.0f}, " \
                         "revenue: {:.2f}, excess_stock: {}, shortages: {}, unit_cost: {}, quantity_on_hand: {}, " \
                         "currency_code: {}, total_orders: {}, backlog: {})"
        return representation.format(self.__sku_id,
                                     self.__average_order,
                                     self.__orders_standard_deviation,
                                     self.__safety_stock,
                                     self.__demand_variability,
                                     self.__reorder_level,
                                     self.__fixed_reorder_quantity,
                                     self.__sku_revenue,
                                     self.__excess_stock,
                                     self.__shortage_qty,
                                     self.__unit_cost,
                                     self.__quantity_on_hand,
                                     self.__currency,
                                     self.__total_orders,
                                     self.__backlog)

    def __iter__(self):
        for original_order in self.__orders.get("demand"):
            yield original_order

    def __len__(self):
        return len(self.__orders.get("demand"))

    def __del__(self):

        self.__orders = None
        self.__sku_id = None
        self.__lead_time = None
        self.__unit_cost = None
        self.__z_value = None
        self.__count_orders = None
        self.__average_order = None
        self.__orders_standard_deviation = None
        self.__safety_stock = None
        self.__demand_variability = None
        self.__reorder_level = None
        self.__reorder_cost = None
        self.__fixed_reorder_quantity = None
