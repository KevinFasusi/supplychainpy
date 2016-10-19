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

from decimal import Decimal
from decimal import ROUND_FLOOR
from decimal import getcontext

import numpy as np
from supplychainpy._helpers._enum_formats import PeriodFormats
from supplychainpy.simulations import simulation_window


# assumptions: opening stock in first period is average stock adjusted to period used in monte carlo if different from
# orders analysis. There are no deliveries in the first period (maybe add switch so there always is a delivery in first,
# users choice) period based on inventory rules.


class SetupMonteCarlo:
    """ Create a monte carlo simulation for inventory analysis."""

    _conversion = 1
    _window = {}

    def __init__(self, analysed_orders: list, period: str = PeriodFormats.months.name, period_length: int = 12):
        self._analysed_orders = analysed_orders
        self._normal_random_distribution = self.generate_normal_random_distribution(period_length=period_length)

    @property
    def normal_random_distribution(self):
        return self._normal_random_distribution

    def generate_normal_random_distribution(self, period_length: int) -> list:

        """ Generates the random demand for a given sku.

        For each sku a set of random demands are calculated based on the normal distribution of demand for this product.

        Args:
            period_length (int):    length of window e.g. 12 weeks for a quarter etc.


        Returns:
            list:   A list of randomly generated demand.



        Raises:
            ValueError:

        """
        orders_normal_distribution = {}
        random_orders_generator = []
        final_random_orders_generator = []
        for sku in self._analysed_orders:
            for i in range(0, period_length):
                nrd_orders = np.random.normal(loc=sku.average_orders,
                                              scale=sku.standard_deviation,
                                              size=sku.order_count)

                random_orders_generator.append(abs(np.array(nrd_orders)).tolist())
            orders_normal_distribution[sku.sku_id] = random_orders_generator
            random_orders_generator = []
        final_random_orders_generator.append(orders_normal_distribution)
        return final_random_orders_generator

    # replace implementation with yield generators instead

    def build_window(self, random_normal_demand: list, period_length: int = 0,
                     holding_cost_percentage: Decimal = 0.48,
                     shortage_cost_percentage: Decimal = 0.3) -> dict:

        """ Builds the simulation window for opening stock, demand, closing stock, backlog, holding cost and shortages.

        The window represents a fixed time frame, supplied by the user. The window is then run several times to generate
        probabilities for example the probability of stocking out during the period specified or the probability that the
        final closing stock will be negative. The results will indicate the accuracy of the analytical model used to
        calculate the safety stock etc, based on a few assumptions.

        Args:
            random_normal_demand (list):        A list of random demand normally distributed.
            period_length (int):                length of window e.g. 12 weeks for a quarter etc.
            holding_cost_percentage (Decimal):  The percentage of unit cost to associate with holding cost,
            shortage_cost_percentage (Decimal): The percentage of unit cost to associate with shortage cost,

        Returns:
            dict:   The build_window returns a dictionary of lists for opening_stock, demand, delivery,closing stock,
                    backlog, holding cost, shortage cost.



        Raises:
            ValueError:     The period_length is currently {} and the actual length of the demand is {}.
                            Please make sure that the two values are equal".format(period_length,
                            len(random_normal_demand[0][sku.sku_id]))
        """

        getcontext().prec = 7
        getcontext().rounding = ROUND_FLOOR

        clist = []

        revenue = lambda unit_cost, units_sold,: Decimal(unit_cost) * Decimal(units_sold)

        # lambda functions for calculating the main values in the monte carlo analysis
        closing_stock = lambda opening_stock, orders, deliveries, backlog: Decimal((Decimal(opening_stock)
                                                                                    - Decimal(orders)) + Decimal(
            deliveries)) - Decimal(backlog) if Decimal((Decimal(opening_stock) - Decimal(orders)) +
                                                       Decimal(deliveries)) - Decimal(backlog) > 0 else 0

        backlog = lambda opening_stock, deliveries, demand: Decimal(abs(
            (Decimal(opening_stock + deliveries)) - Decimal(demand))) if \
            Decimal((opening_stock + deliveries)) - Decimal(demand) < 0 else 0

        holding_cost = lambda cls_stock, unit_cost: cls_stock * (
            Decimal(unit_cost) * Decimal(holding_cost_percentage)) if cls_stock > 0 else 0

        shortages = lambda opening_stock, orders, deliveries: abs((Decimal(opening_stock) - Decimal(orders)) +
                                                                  Decimal(deliveries)) if \
            ((Decimal(opening_stock) - Decimal(orders)) + Decimal(deliveries)) < 0 else 0

        # shortage cost as a percentage of unit cost. Increase to percentage to have a bigger affect change more
        shortage_cost = lambda cls_stock, unit_cost: cls_stock * (
            Decimal(unit_cost) * Decimal(shortage_cost_percentage)) if int(cls_stock) > 0 else 0

        raise_po = lambda reorder_lvl, cls_stock: True if cls_stock <= reorder_lvl else False

        po_qty = lambda eoq, reorder_lvl, backlog, cls_stock: Decimal(eoq) + Decimal(backlog) + Decimal(
            (Decimal(reorder_lvl) - Decimal(cls_stock))) if Decimal(eoq) + Decimal(backlog) + Decimal(
            (Decimal(reorder_lvl) - Decimal(cls_stock))) > 0 else 0

        # calculate period to receive po and quantity to receive

        for sku in self._analysed_orders:
            if period_length != len(random_normal_demand[0][sku.sku_id]):
                raise ValueError("The period_length is currently {} and the actual length of the demand is {}. "
                                 "Please make sure that the two values are equal".format(period_length,
                                                                                         len(random_normal_demand[0][
                                                                                                 sku.sku_id])))

        sim_frame_collection = []
        index_item = 1
        for sku in self._analysed_orders:

            period = 1
            order_receipt_index = {}
            final_stock = 0
            sim_window_collection = {}
            previous_backlog = Decimal('0')
            order_receipt_index = {}
            # create the sim_window for each sku, suing the random normal demand generated
            for i in range(0, period_length):

                po_qty_raised = 0

                # instantiate sim_window
                sim_window = simulation_window.MonteCarloWindow

                # add sku_id
                sim_window.sku_id = sku.sku_id

                # add closing stock
                previous_closing_stock = final_stock

                # mark sim_window.position or period in analysis
                sim_window.position = period

                # add average orders to opening_stock if first period else add closing stock
                if sim_window.position == 1:
                    sim_window.opening_stock = (sku.reorder_level - Decimal(sku.safety_stock)) + Decimal(sku.safety_stock) #calculated ltd until put into analyse orders
                else:
                    sim_window.opening_stock = previous_closing_stock

                # add random demand
                demand = random_normal_demand[0][sku.sku_id][i][0]
                sim_window.demand = demand

                #
                if sim_window.position in order_receipt_index.keys():
                    sim_window.purchase_order_receipt_qty = order_receipt_index[sim_window.position]
                    sim_window.po_number_received = 'PO {:.0f}{}'.format(sim_window.position, sim_window.index)
                    del order_receipt_index[sim_window.position]
                else:
                    sim_window.purchase_order_receipt_qty = 0
                    sim_window.po_number_received = ''

                sim_window.index = index_item

                sim_window.backlog = backlog(opening_stock=sim_window.opening_stock,
                                             deliveries=sim_window.purchase_order_receipt_qty,
                                             demand=demand) + previous_backlog
                sim_window.closing_stock = closing_stock(opening_stock=sim_window.opening_stock,
                                                         orders=demand,
                                                         deliveries=sim_window.purchase_order_receipt_qty,
                                                         backlog=sim_window.backlog)

                sim_window.holding_cost = holding_cost(sim_window.closing_stock, sku.unit_cost)

                sim_window.shortage_units = shortages(opening_stock=sim_window.opening_stock,
                                                      orders=demand,
                                                      deliveries=sim_window.purchase_order_receipt_qty)

                sim_window.shortage_cost = shortage_cost(cls_stock=(sim_window.backlog - previous_backlog),
                                                         unit_cost=sku.unit_cost)

                sim_window.po_raised_flag = raise_po(reorder_lvl=sku.reorder_level, cls_stock=sim_window.closing_stock)

                po_receipt_period = period + sku.lead_time

                po_qty_raised = po_qty(eoq=sku.economic_order_qty,
                                       reorder_lvl=sku.reorder_level,
                                       backlog=sim_window.backlog,
                                       cls_stock=sim_window.closing_stock)

                if po_qty_raised > 0:
                    order_receipt_index.update({po_receipt_period: po_qty_raised})
                    sim_window.purchase_order_raised_qty = order_receipt_index.get(po_receipt_period)
                else:
                    sim_window.purchase_order_raised_qty = 0

                sim_window.po_number_raised = ''

                if int(sim_window.purchase_order_raised_qty) > 0:
                    sim_window.po_number_raised = 'PO {:.0f}{}'.format(po_receipt_period, sim_window.index)
                    del po_receipt_period

                final_stock = sim_window.closing_stock

                if int(sim_window.closing_stock) == 0:
                    previous_backlog += sim_window.backlog
                else:
                    previous_backlog = 0

                units_sold = self._units_sold(backlog=sim_window.backlog, opening_stock=sim_window.opening_stock,
                                              delivery=sim_window.purchase_order_receipt_qty, demand=sim_window.demand)
                sim_window.sold = units_sold
                sim_window.revenue = Decimal(revenue(sku.unit_cost, units_sold))
                yield sim_window

                del sim_window
                del po_qty_raised
                period += 1

            index_item += 1

    def _units_sold(self, backlog, opening_stock, delivery, demand):

        # check if opening_stock + closing_stock = 0
        if int(opening_stock) + int(delivery) == 0:
            sold = 0.00
        else:
            sold = (opening_stock + delivery) - Decimal(demand) - Decimal(backlog)

        if sold < 0:
            units_sold = Decimal(demand) + Decimal(backlog) - Decimal(abs(sold))
        else:
            units_sold = Decimal(sold)

        return units_sold
