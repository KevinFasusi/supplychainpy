import numpy as np
from decimal import Decimal

from supplychainpy.demand.abc_xyz import AbcXyz
from supplychainpy.enum_formats import PeriodFormats
from supplychainpy.simulations import simulation_window

# assumptions: opening stock in first period is average stock adjusted to period used in monte carlo if different from
# orders analysis. There are no deliveries in the first period (maybe add switch so there always is a delivery in first,
# users choice) period based on inventory rules.


class SetupMonteCarlo:
    """ Create a monte carlo simulation for inventory analysis."""

    _conversion = 1
    _window = {}

    def __init__(self, analysed_orders: AbcXyz, period: str = PeriodFormats.months.name, period_length: int = 12):
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
        # lambda functions for calculating the main values in the monte carlo analysis
        closing_stock = lambda opening_stock, orders, deliveries, backlog: Decimal((Decimal(opening_stock)
                                                                                    - Decimal(orders)) + Decimal(
            deliveries)) - Decimal(backlog)

        backlog = lambda opening_stock, deliveries, demand: abs(
            (Decimal(opening_stock + deliveries)) - Decimal(demand)) if \
            Decimal((opening_stock + deliveries)) - Decimal(demand) < 0 else 0

        holding_cost = lambda cls_stock, unit_cost: cls_stock * (
            Decimal(unit_cost) * Decimal(holding_cost_percentage)) if cls_stock > 0 else 0

        shortages = lambda opening_stock, orders, deliveries: abs((Decimal(opening_stock) - Decimal(orders)) +
                                                                  Decimal(deliveries)) if \
            ((Decimal(opening_stock) - Decimal(orders)) + Decimal(deliveries)) < 0 else 0

        shortage_cost = lambda cls_stock, unit_cost: cls_stock * (
            Decimal(unit_cost) * Decimal(shortage_cost_percentage)) if cls_stock > 0 else 0

        raise_po = lambda reorder_lvl, cls_stock: True if cls_stock <= reorder_lvl else False

        po_qty = lambda eoq, reorder_lvl, backlog, cls_stock: Decimal(eoq) + Decimal(backlog) + Decimal(
            (Decimal(reorder_lvl) - Decimal(cls_stock))) if Decimal(eoq) + Decimal(backlog) + Decimal(
            (Decimal(reorder_lvl) - Decimal(cls_stock))) > 0 else 0

        # calculate period to recieve po and quantity to receiv

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

            # create the sim_window for each sku, suing the random normal demand generated
            for i in range(0, period_length):
                sim_window = simulation_window.MonteCarloWindow
                sim_window.sku_id = sku.sku_id
                previous_closing_stock = final_stock
                sim_window.position = period
                if sim_window.position == 1:
                    sim_window.opening_stock = sku.average_orders
                else:
                    sim_window.opening_stock = previous_closing_stock

                demand = random_normal_demand[0][sku.sku_id][i][0]

                sim_window.demand = demand

                if sim_window.position in order_receipt_index.keys():
                    sim_window.purchase_order_receipt_qty = order_receipt_index[sim_window.position]
                    order_receipt_index.pop(sim_window.position)
                else:
                    sim_window.purchase_order_receipt_qty = 0

                sim_window.index = index_item

                sim_window.backlog = backlog(opening_stock=sim_window.opening_stock,
                                             deliveries=sim_window.purchase_order_receipt_qty, demand=demand)
                sim_window.closing_stock = closing_stock(opening_stock=sim_window.opening_stock,
                                                         orders=demand,
                                                         deliveries=sim_window.purchase_order_receipt_qty,
                                                         backlog=sim_window.backlog)

                sim_window.holding_cost = holding_cost(sim_window.closing_stock, sku.unit_cost)

                sim_window.shortage_units = shortages(opening_stock=sim_window.opening_stock,
                                                      orders=demand,
                                                      deliveries=sim_window.purchase_order_receipt_qty)

                sim_window.shortage_cost = shortage_cost(cls_stock=sim_window.closing_stock, unit_cost=sku.unit_cost)

                sim_window.po_raised_flag = raise_po(reorder_lvl=sku.reorder_level, cls_stock=sim_window.closing_stock)

                po_receipt_period = period + sku.lead_time

                order_receipt_index[po_receipt_period] = po_qty(eoq=sku.economic_order_qty,
                                                                reorder_lvl=sku.reorder_level,
                                                                backlog=sim_window.backlog,
                                                                cls_stock=sim_window.closing_stock)

                final_stock = sim_window.closing_stock

                yield sim_window

                period += 1
            index_item += 1
